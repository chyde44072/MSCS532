# Shared Resources
# Common stuff used across both phases of the project

"""
Shared Resources Package

Common utilities and data that both phases need:

- Horse: Data model for horse entities
- Data loading utilities: For the Kentucky Derby dataset
- Shared constants and helper functions

Usage:
    from shared import Horse
    from shared.utils.data_loader import load_kentucky_derby_data
    
    # Load the horse data
    horses = load_kentucky_derby_data()
"""

__version__ = "1.0.0"
__author__ = "MSCS532 Student"

# Import common utilities
try:
    from .models.horse import Horse
    
    __all__ = ['Horse']
    
except ImportError:
    __all__ = []
