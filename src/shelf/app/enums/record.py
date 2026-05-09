"""Enumerations for record-related entities."""

from enum import Enum


class MediumFormat(str, Enum):
    """Enum for Medium formats."""

    VINYL = 'vinyl'
    CD = 'cd'
    CASSETTE = 'cassette'


class RecordGrade(str, Enum):
    """Enum for Record grades."""

    M = 'M'  # Mint
    NM = 'NM'  # Near Mint
    VG_PLUS = 'VG+'  # Very Good Plus
    VG = 'VG'  # Very Good
    G_PLUS = 'G+'  # Good Plus
    G = 'G'  # Good
    F = 'F'  # Fair
    P = 'P'  # Poor


class SleeveGrade(str, Enum):
    """Enum for Sleeve grades."""

    SS = 'SS'  # Still Sealed
    M = 'M'  # Mint
    NM = 'NM'  # Near Mint
    VG_PLUS = 'VG+'  # Very Good Plus
    VG = 'VG'  # Very Good
    G_PLUS = 'G+'  # Good Plus
    G = 'G'  # Good
    F = 'F'  # Fair
    P = 'P'  # Poor
