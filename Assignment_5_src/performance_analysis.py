import random
import time
import matplotlib.pyplot as plt
import numpy as np
from typing import List, Dict, Tuple, Callable
from quicksort import QuickSort, time_sorting_algorithm
import statistics


class PerformanceAnalyzer:
    """
    A class for analyzing and comparing the performance of Quicksort algorithms.
    """
    
    def __init__(self):
        self.quicksort = QuickSort()
        self.results = {}
    
    def generate_test_data(self, size: int, data_type: str) -> List[int]:
        """
        Generate test data of specified size and distribution type.
        
        Args:
            size: Number of elements to generate
            data_type: Type of data distribution
                      - 'random': Random integers
                      - 'sorted': Already sorted array
                      - 'reverse': Reverse sorted array
                      - 'nearly_sorted': Array with few out-of-place elements
                      - 'duplicates': Array with many duplicate values
                      
        Returns:
            List of integers according to specified distribution
        """
        if data_type == 'random':
            return [random.randint(1, size * 10) for _ in range(size)]
        
        elif data_type == 'sorted':
            return list(range(1, size + 1))
        
        elif data_type == 'reverse':
            return list(range(size, 0, -1))
        
        elif data_type == 'nearly_sorted':
            # Create sorted array and swap a few random pairs
            arr = list(range(1, size + 1))
            num_swaps = max(1, size // 20)  # 5% of elements
            for _ in range(num_swaps):
                i, j = random.sample(range(size), 2)
                arr[i], arr[j] = arr[j], arr[i]
            return arr
        
        elif data_type == 'duplicates':
            # Array with many duplicate values
            unique_values = size // 10 if size >= 10 else 1
            return [random.randint(1, unique_values) for _ in range(size)]
        
        else:
            raise ValueError(f"Unknown data type: {data_type}")
    
    def run_single_test(self, algorithm: Callable, data: List[int], num_runs: int = 5) -> Dict:
        """
        Run a single test multiple times and return average statistics.
        
        Args:
            algorithm: Sorting algorithm to test
            data: Test data
            num_runs: Number of times to run the test
            
        Returns:
            Dictionary containing average performance metrics
        """
        times = []
        comparisons_list = []
        swaps_list = []
        recursive_calls_list = []
        
        for _ in range(num_runs):
            exec_time, _, stats = time_sorting_algorithm(algorithm, data)
            times.append(exec_time)
            comparisons_list.append(stats['comparisons'])
            swaps_list.append(stats['swaps'])
            recursive_calls_list.append(stats['recursive_calls'])
        
        return {
            'avg_time': statistics.mean(times),
            'std_time': statistics.stdev(times) if len(times) > 1 else 0,
            'avg_comparisons': statistics.mean(comparisons_list),
            'avg_swaps': statistics.mean(swaps_list),
            'avg_recursive_calls': statistics.mean(recursive_calls_list),
            'min_time': min(times),
            'max_time': max(times)
        }
    
    def comprehensive_analysis(self, sizes: List[int] = None, data_types: List[str] = None) -> Dict:
        """
        Perform comprehensive analysis across different sizes and data types.
        
        Args:
            sizes: List of array sizes to test
            data_types: List of data distribution types to test
            
        Returns:
            Dictionary containing all test results
        """
        if sizes is None:
            sizes = [100, 500, 1000, 2000, 5000]
        
        if data_types is None:
            data_types = ['random', 'sorted', 'reverse', 'nearly_sorted', 'duplicates']
        
        results = {
            'deterministic': {},
            'randomized': {}
        }
        
        total_tests = len(sizes) * len(data_types)
        test_count = 0
        
        print("Starting comprehensive performance analysis...")
        print(f"Testing {len(sizes)} sizes × {len(data_types)} data types = {total_tests} test configurations")
        print("Each configuration runs 5 times for statistical reliability\n")
        
        for size in sizes:
            print(f"Testing array size: {size}")
            
            for data_type in data_types:
                test_count += 1
                print(f"  Progress: {test_count}/{total_tests} - Data type: {data_type}")
                
                # Generate test data
                test_data = self.generate_test_data(size, data_type)
                
                # Test deterministic quicksort
                det_results = self.run_single_test(
                    self.quicksort.deterministic_quicksort, test_data
                )
                
                # Test randomized quicksort
                rand_results = self.run_single_test(
                    self.quicksort.randomized_quicksort, test_data
                )
                
                # Store results
                if size not in results['deterministic']:
                    results['deterministic'][size] = {}
                    results['randomized'][size] = {}
                
                results['deterministic'][size][data_type] = det_results
                results['randomized'][size][data_type] = rand_results
        
        print("\nAnalysis complete!")
        self.results = results
        return results
    
    def print_summary_table(self):
        """Print a summary table of results."""
        if not self.results:
            print("No results available. Run comprehensive_analysis first.")
            return
        
        print("\n" + "="*80)
        print("PERFORMANCE ANALYSIS SUMMARY")
        print("="*80)
        
        # Print header
        print(f"{'Size':<8} {'Data Type':<15} {'Algorithm':<12} {'Avg Time (s)':<12} {'Comparisons':<12} {'Swaps':<8}")
        print("-" * 80)
        
        for size in sorted(self.results['deterministic'].keys()):
            for data_type in self.results['deterministic'][size].keys():
                # Deterministic results
                det_stats = self.results['deterministic'][size][data_type]
                print(f"{size:<8} {data_type:<15} {'Deterministic':<12} "
                      f"{det_stats['avg_time']:<12.6f} {det_stats['avg_comparisons']:<12.0f} "
                      f"{det_stats['avg_swaps']:<8.0f}")
                
                # Randomized results
                rand_stats = self.results['randomized'][size][data_type]
                print(f"{'':<8} {'':<15} {'Randomized':<12} "
                      f"{rand_stats['avg_time']:<12.6f} {rand_stats['avg_comparisons']:<12.0f} "
                      f"{rand_stats['avg_swaps']:<8.0f}")
                print()
    
    def generate_performance_plots(self, save_plots: bool = True):
        """Generate and display performance comparison plots."""
        if not self.results:
            print("No results available. Run comprehensive_analysis first.")
            return
        
        try:
            import matplotlib.pyplot as plt
        except ImportError:
            print("Matplotlib not available. Install with: pip install matplotlib")
            return
        
        # Create subplots for different metrics
        fig, axes = plt.subplots(2, 2, figsize=(15, 12))
        fig.suptitle('Quicksort Performance Analysis', fontsize=16)
        
        sizes = sorted(self.results['deterministic'].keys())
        data_types = ['random', 'sorted', 'reverse', 'nearly_sorted', 'duplicates']
        
        # Plot 1: Average execution time vs array size for random data
        ax1 = axes[0, 0]
        det_times = [self.results['deterministic'][size]['random']['avg_time'] for size in sizes]
        rand_times = [self.results['randomized'][size]['random']['avg_time'] for size in sizes]
        
        ax1.plot(sizes, det_times, 'b-o', label='Deterministic', linewidth=2)
        ax1.plot(sizes, rand_times, 'r-s', label='Randomized', linewidth=2)
        ax1.set_xlabel('Array Size')
        ax1.set_ylabel('Average Time (seconds)')
        ax1.set_title('Execution Time vs Array Size (Random Data)')
        ax1.legend()
        ax1.grid(True, alpha=0.3)
        
        # Plot 2: Comparisons for different data types (size = 1000)
        ax2 = axes[0, 1]
        if 1000 in self.results['deterministic']:
            det_comps = [self.results['deterministic'][1000][dt]['avg_comparisons'] for dt in data_types]
            rand_comps = [self.results['randomized'][1000][dt]['avg_comparisons'] for dt in data_types]
            
            x = np.arange(len(data_types))
            width = 0.35
            
            ax2.bar(x - width/2, det_comps, width, label='Deterministic', alpha=0.8)
            ax2.bar(x + width/2, rand_comps, width, label='Randomized', alpha=0.8)
            ax2.set_xlabel('Data Type')
            ax2.set_ylabel('Average Comparisons')
            ax2.set_title('Comparisons by Data Type (Size=1000)')
            ax2.set_xticks(x)
            ax2.set_xticklabels(data_types, rotation=45)
            ax2.legend()
        
        # Plot 3: Time complexity visualization for worst case (reverse sorted)
        ax3 = axes[1, 0]
        det_times_reverse = [self.results['deterministic'][size]['reverse']['avg_time'] for size in sizes]
        rand_times_reverse = [self.results['randomized'][size]['reverse']['avg_time'] for size in sizes]
        
        ax3.plot(sizes, det_times_reverse, 'b-o', label='Deterministic (Reverse)', linewidth=2)
        ax3.plot(sizes, rand_times_reverse, 'r-s', label='Randomized (Reverse)', linewidth=2)
        
        # Add theoretical O(n²) and O(n log n) lines for reference
        n_squared = [(size/sizes[0])**2 * det_times_reverse[0] for size in sizes]
        n_log_n = [(size * np.log(size)) / (sizes[0] * np.log(sizes[0])) * rand_times_reverse[0] for size in sizes]
        
        ax3.plot(sizes, n_squared, 'b--', alpha=0.5, label='O(n²) reference')
        ax3.plot(sizes, n_log_n, 'r--', alpha=0.5, label='O(n log n) reference')
        
        ax3.set_xlabel('Array Size')
        ax3.set_ylabel('Average Time (seconds)')
        ax3.set_title('Worst Case Performance (Reverse Sorted)')
        ax3.legend()
        ax3.grid(True, alpha=0.3)
        
        # Plot 4: Recursive calls comparison
        ax4 = axes[1, 1]
        det_calls = [self.results['deterministic'][size]['random']['avg_recursive_calls'] for size in sizes]
        rand_calls = [self.results['randomized'][size]['random']['avg_recursive_calls'] for size in sizes]
        
        ax4.plot(sizes, det_calls, 'b-o', label='Deterministic', linewidth=2)
        ax4.plot(sizes, rand_calls, 'r-s', label='Randomized', linewidth=2)
        ax4.set_xlabel('Array Size')
        ax4.set_ylabel('Average Recursive Calls')
        ax4.set_title('Recursive Calls vs Array Size (Random Data)')
        ax4.legend()
        ax4.grid(True, alpha=0.3)
        
        plt.tight_layout()
        
        if save_plots:
            plt.savefig('quicksort_performance_analysis.png', dpi=300, bbox_inches='tight')
            print("Performance plots saved as 'quicksort_performance_analysis.png'")
        
        plt.show()
    
    def analyze_randomization_benefit(self):
        """Analyze the specific benefits of randomization."""
        if not self.results:
            print("No results available. Run comprehensive_analysis first.")
            return
        
        print("\n" + "="*60)
        print("RANDOMIZATION BENEFIT ANALYSIS")
        print("="*60)
        
        data_types = ['sorted', 'reverse']  # Worst-case scenarios for deterministic
        
        for data_type in data_types:
            print(f"\n{data_type.upper()} DATA ANALYSIS:")
            print("-" * 40)
            
            for size in sorted(self.results['deterministic'].keys()):
                det_time = self.results['deterministic'][size][data_type]['avg_time']
                rand_time = self.results['randomized'][size][data_type]['avg_time']
                
                improvement = ((det_time - rand_time) / det_time) * 100
                
                print(f"Size {size:>5}: Deterministic={det_time:.6f}s, "
                      f"Randomized={rand_time:.6f}s, "
                      f"Improvement={improvement:>6.1f}%")


def main():
    """Main function to run comprehensive performance analysis."""
    print("Quicksort Performance Analysis")
    print("=" * 50)
    
    analyzer = PerformanceAnalyzer()
    
    # Run comprehensive analysis
    # Note: Using smaller sizes for demonstration. Increase for more comprehensive analysis.
    test_sizes = [100, 500, 1000, 2000]
    test_data_types = ['random', 'sorted', 'reverse', 'nearly_sorted', 'duplicates']
    
    results = analyzer.comprehensive_analysis(sizes=test_sizes, data_types=test_data_types)
    
    # Print summary
    analyzer.print_summary_table()
    
    # Analyze randomization benefits
    analyzer.analyze_randomization_benefit()
    
    # Generate plots (will skip if matplotlib not available)
    try:
        analyzer.generate_performance_plots()
    except Exception as e:
        print(f"\nPlot generation skipped: {e}")
        print("Install matplotlib with: pip install matplotlib")


if __name__ == "__main__":
    main()
