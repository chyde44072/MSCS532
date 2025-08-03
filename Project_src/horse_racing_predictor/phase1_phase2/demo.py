"""
Horse Racing Predictor - Proof of Concept Demonstration
Enhanced demonstration using real Kentucky Derby winner data.
"""

from data_structures.hash_table import HorseDatabase
from data_structures.leaderboard_heap import Leaderboard
from data_structures.avl_tree import AVLTree
import sys
import os
sys.path.append(os.path.join(os.path.dirname(__file__), '..', 'shared'))
from utils.data_loader import load_kentucky_derby_data, get_horse_stats_summary, filter_horses_by_criteria, create_sample_race

def print_section_header(title: str):
    """Print a formatted section header."""
    print("\n" + "=" * 70)
    print(f" {title}")
    print("=" * 70)

def demonstrate_data_loading():
    """Demonstrate loading and analyzing the Kentucky Derby data."""
    print_section_header("KENTUCKY DERBY DATA ANALYSIS")
    
    horses, race_times = load_kentucky_derby_data()
    
    print(f"✅ Loaded {len(horses)} Kentucky Derby winners")
    print(f"✅ Generated {len(race_times)} race time records")
    
    # Show summary statistics
    stats = get_horse_stats_summary(horses)
    print(f"\n📊 Dataset Summary:")
    print(f"   Average Speed: {stats['avg_speed']['min']:.1f} - {stats['avg_speed']['max']:.1f} mph (avg: {stats['avg_speed']['mean']:.1f})")
    print(f"   Win Ratios: {stats['win_ratio']['min']:.2f} - {stats['win_ratio']['max']:.2f} (avg: {stats['win_ratio']['mean']:.2f})")
    print(f"   Horse Ages: {stats['age_distribution']['min']} - {stats['age_distribution']['max']} years")
    
    # Show top performers
    print(f"\n🏆 Top 5 Horses by Speed:")
    speed_sorted = sorted(horses, key=lambda x: x[1]['avg_speed'], reverse=True)
    for i, (horse_id, data) in enumerate(speed_sorted[:5], 1):
        print(f"   {i}. {data['name']}: {data['avg_speed']} mph (Win ratio: {data['win_ratio']:.2f})")
    
    return horses, race_times

def demonstrate_hash_table_with_real_data(horses):
    """Demonstrate hash table operations with Kentucky Derby data."""
    print_section_header("HASH TABLE OPERATIONS - KENTUCKY DERBY DATABASE")
    
    db = HorseDatabase()
    
    # Load all horses
    print("📥 Loading Kentucky Derby winners into database...")
    for horse_id, data in horses:
        db.add_horse(horse_id, data)
    
    print(f"✅ Successfully loaded {len(db)} horse profiles")
    
    # Demonstrate specific lookups
    print(f"\n🔍 Horse Profile Lookups:")
    famous_horses = ["H011", "H008", "H020"]  # American Pharoah, Justify, Barbaro
    
    for horse_id in famous_horses:
        horse_data = db.get_horse(horse_id)
        if horse_data:
            print(f"   {horse_data['name']} ({horse_id}):")
            print(f"     Speed: {horse_data['avg_speed']} mph | Win Rate: {horse_data['win_ratio']:.1%}")
            print(f"     Record: {horse_data['total_wins']}/{horse_data['total_races']} | Age: {horse_data['age']}")
    
    # Demonstrate performance updates
    print(f"\n📈 Performance Updates:")
    update_horse = "H011"  # American Pharoah
    original_data = db.get_horse(update_horse)
    
    db.update_performance(update_horse, {
        "latest_race_time": 120.45,
        "latest_race_date": "2024-07-15",
        "current_form": "excellent",
        "recent_workouts": ["59.2s", "58.8s", "59.5s"]
    })
    
    updated_data = db.get_horse(update_horse)
    print(f"   Updated {updated_data['name']} with latest race data")
    print(f"   Latest race time: {updated_data['latest_race_time']}s")
    print(f"   Current form: {updated_data['current_form']}")
    
    return db

def demonstrate_leaderboard_with_real_data(leaderboard, db, race_times):
    """Demonstrate leaderboard operations with real race times."""
    print_section_header("LEADERBOARD OPERATIONS - RACE TIME RANKINGS")
    
    # Add all race times
    print("⏱️  Adding race times to leaderboard...")
    for horse_id, time in race_times:
        leaderboard.add_result(horse_id, time)
    
    print(f"✅ Added {leaderboard.size()} race results")
    
    # Show fastest horses
    print(f"\n🏃 Fastest Race Times (Top 8):")
    top_performers = leaderboard.get_top_performers(8)
    
    for i, (time, horse_id) in enumerate(top_performers, 1):
        horse_data = db.get_horse(horse_id)
        print(f"   {i:2d}. {horse_data['name']:<18} {time:6.2f}s (Speed: {horse_data['avg_speed']} mph)")
    
    # Demonstrate rank queries
    print(f"\n📊 Individual Rankings:")
    check_horses = ["H003", "H020", "H011", "H017"]  # Mage, Barbaro, American Pharoah, Mine That Bird
    
    for horse_id in check_horses:
        rank = leaderboard.get_horse_rank(horse_id)
        horse_data = db.get_horse(horse_id)
        print(f"   {horse_data['name']:<18} is ranked #{rank:2d}")
    
    # Simulate race improvement
    print(f"\n⚡ Simulating Performance Improvement:")
    improve_horse = "H002"  # Mystik Dan
    horse_data = db.get_horse(improve_horse)
    original_rank = leaderboard.get_horse_rank(improve_horse)
    
    # Improve time by 3 seconds
    current_times = leaderboard.get_all_results()
    current_time = next(time for time, h_id in current_times if h_id == improve_horse)
    improved_time = current_time - 3.0
    
    leaderboard.add_result(improve_horse, improved_time)
    new_rank = leaderboard.get_horse_rank(improve_horse)
    
    print(f"   {horse_data['name']} improved from {current_time:.2f}s to {improved_time:.2f}s")
    print(f"   Rank improved from #{original_rank} to #{new_rank}")
    
    return leaderboard

def demonstrate_avl_tree_with_real_data(ranking_tree, db, horses):
    """Demonstrate AVL tree operations with win ratio rankings."""
    print_section_header("AVL TREE OPERATIONS - WIN RATIO ANALYSIS")
    
    # Insert all horses by win ratio
    print("🌳 Building win ratio ranking tree...")
    for horse_id, data in horses:
        ranking_tree.insert(horse_id, data['win_ratio'])
    
    print(f"✅ Added {len(horses)} horses to ranking tree")
    
    # Range queries for different performance tiers
    print(f"\n📈 Performance Tier Analysis:")
    
    # Elite performers (win ratio >= 0.67)
    elite = ranking_tree.get_range(0.67, 1.0)
    print(f"   🥇 Elite Performers (≥67% win rate): {len(elite)} horses")
    for horse_id, ratio in sorted(elite, key=lambda x: x[1], reverse=True):
        horse_data = db.get_horse(horse_id)
        print(f"      {horse_data['name']:<18} {ratio:.1%} ({horse_data['total_wins']}/{horse_data['total_races']})")
    
    # Good performers (0.63-0.66)
    good = ranking_tree.get_range(0.63, 0.66)
    print(f"\n   🥈 Good Performers (63-66% win rate): {len(good)} horses")
    for horse_id, ratio in sorted(good, key=lambda x: x[1], reverse=True)[:5]:  # Show top 5
        horse_data = db.get_horse(horse_id)
        print(f"      {horse_data['name']:<18} {ratio:.1%}")
    
    # Average performers (0.59-0.62)
    average = ranking_tree.get_range(0.59, 0.62)
    print(f"\n   🥉 Average Performers (59-62% win rate): {len(average)} horses")
    
    # Complete ranking
    print(f"\n🏆 Complete Win Ratio Rankings (Top 10):")
    all_ranked = ranking_tree.get_sorted_list()
    all_ranked.reverse()  # Highest first
    
    for i, (horse_id, ratio) in enumerate(all_ranked[:10], 1):
        horse_data = db.get_horse(horse_id)
        speed = horse_data['avg_speed']
        print(f"   {i:2d}. {horse_data['name']:<18} {ratio:.1%} | {speed} mph")
    
    return ranking_tree

def demonstrate_advanced_analysis(db, leaderboard, ranking_tree):
    """Demonstrate advanced analysis combining all data structures."""
    print_section_header("ADVANCED PERFORMANCE ANALYSIS")
    
    # Find horses that excel in both speed and consistency
    print("🔍 Elite Multi-Dimensional Analysis:")
    print("    Finding horses with exceptional speed AND high win rates...")
    
    # Get top speed performers
    top_speed_horses = []
    all_horses = db.list_horses()
    
    for horse_id in all_horses:
        horse_data = db.get_horse(horse_id)
        if horse_data['avg_speed'] >= 37.0:  # Top speed threshold
            top_speed_horses.append((horse_id, horse_data['avg_speed']))
    
    # Check their win ratios
    elite_combo = []
    for horse_id, speed in top_speed_horses:
        horse_data = db.get_horse(horse_id)
        if horse_data['win_ratio'] >= 0.65:  # High win rate threshold
            rank = leaderboard.get_horse_rank(horse_id)
            elite_combo.append((horse_id, speed, horse_data['win_ratio'], rank))
    
    print(f"\n⭐ Elite Speed + Consistency Champions ({len(elite_combo)} horses):")
    elite_combo.sort(key=lambda x: (x[1], x[2]), reverse=True)  # Sort by speed, then win ratio
    
    for horse_id, speed, win_ratio, rank in elite_combo:
        horse_data = db.get_horse(horse_id)
        print(f"   🏆 {horse_data['name']:<18} | Speed: {speed} mph | Win Rate: {win_ratio:.1%} | Race Rank: #{rank}")
    
    # Identify improvement candidates
    print(f"\n📊 Improvement Opportunity Analysis:")
    print("    Horses with good speed but inconsistent results...")
    
    improvement_candidates = []
    for horse_id in all_horses:
        horse_data = db.get_horse(horse_id)
        if horse_data['avg_speed'] >= 36.5 and horse_data['win_ratio'] < 0.63:
            improvement_candidates.append((horse_id, horse_data))
    
    improvement_candidates.sort(key=lambda x: x[1]['avg_speed'], reverse=True)
    
    for horse_id, data in improvement_candidates[:5]:
        rank = leaderboard.get_horse_rank(horse_id)
        print(f"   📈 {data['name']:<18} | Speed: {data['avg_speed']} mph | Win Rate: {data['win_ratio']:.1%} | Potential for improvement")
    
    # Performance correlation analysis
    print(f"\n🔬 Speed vs Consistency Correlation:")
    
    high_speed_high_ratio = sum(1 for h_id in all_horses 
                               if db.get_horse(h_id)['avg_speed'] >= 36.8 and db.get_horse(h_id)['win_ratio'] >= 0.65)
    
    high_speed_low_ratio = sum(1 for h_id in all_horses 
                              if db.get_horse(h_id)['avg_speed'] >= 36.8 and db.get_horse(h_id)['win_ratio'] < 0.65)
    
    print(f"   High Speed + High Win Rate: {high_speed_high_ratio} horses")
    print(f"   High Speed + Low Win Rate:  {high_speed_low_ratio} horses")
    print(f"   Analysis: {'Strong' if high_speed_high_ratio > high_speed_low_ratio else 'Weak'} correlation between speed and consistency")

def simulate_race_prediction(db, leaderboard, ranking_tree):
    """Simulate a race prediction scenario."""
    print_section_header("RACE PREDICTION SIMULATION")
    
    horses = [(h_id, db.get_horse(h_id)) for h_id in db.list_horses()]
    
    # Create a sample race
    race_results = create_sample_race(horses, 8)
    
    print("🏁 Simulated Race Setup:")
    print("   Participants:")
    for i, (horse_id, _) in enumerate(race_results, 1):
        horse_data = db.get_horse(horse_id)
        current_rank = leaderboard.get_horse_rank(horse_id)
        print(f"   {i}. {horse_data['name']:<18} | Historical Rank: #{current_rank} | Win Rate: {horse_data['win_ratio']:.1%}")
    
    print(f"\n🏆 Race Results:")
    for position, (horse_id, time) in enumerate(race_results, 1):
        horse_data = db.get_horse(horse_id)
        historical_rank = leaderboard.get_horse_rank(horse_id)
        
        if position <= 3:
            medal = ["🥇", "🥈", "🥉"][position - 1]
        else:
            medal = f"{position:2d}."
        
        print(f"   {medal} {horse_data['name']:<18} {time:6.2f}s (Historical: #{historical_rank})")
    
    # Prediction accuracy analysis
    print(f"\n📊 Prediction Analysis:")
    winner_id = race_results[0][0]
    winner_data = db.get_horse(winner_id)
    winner_historical_rank = leaderboard.get_horse_rank(winner_id)
    
    print(f"   Race Winner: {winner_data['name']}")
    print(f"   Historical Rank: #{winner_historical_rank} out of {leaderboard.size()}")
    print(f"   Win Probability Based on History: {winner_data['win_ratio']:.1%}")
    
    if winner_historical_rank <= 5:
        print(f"   ✅ Prediction Success: Top historical performer won")
    else:
        print(f"   ⚠️  Upset Victory: Lower-ranked horse performed above expectations")

def main():
    """Enhanced main demonstration with real Kentucky Derby data."""
    print("🐎 HORSE RACING PREDICTOR - KENTUCKY DERBY ANALYSIS 🐎")
    print("Advanced data structures demonstration with real racing data")
    
    try:
        # Load real data
        horses, race_times = demonstrate_data_loading()
        
        # Initialize data structures
        horse_db = HorseDatabase()
        leaderboard = Leaderboard()
        ranking_tree = AVLTree()
        
        # Run enhanced demonstrations
        horse_db = demonstrate_hash_table_with_real_data(horses)
        leaderboard = demonstrate_leaderboard_with_real_data(leaderboard, horse_db, race_times)
        ranking_tree = demonstrate_avl_tree_with_real_data(ranking_tree, horse_db, horses)
        
        # Advanced analysis
        demonstrate_advanced_analysis(horse_db, leaderboard, ranking_tree)
        simulate_race_prediction(horse_db, leaderboard, ranking_tree)
        
        print_section_header("DEMONSTRATION COMPLETED SUCCESSFULLY")
        print("✅ All data structures working with real Kentucky Derby data")
        print("✅ Performance analysis and prediction capabilities demonstrated")
        print("✅ System ready for advanced horse racing prediction algorithms")
        
    except Exception as e:
        print(f"\n❌ Error during demonstration: {e}")
        import traceback
        traceback.print_exc()

if __name__ == "__main__":
    main()