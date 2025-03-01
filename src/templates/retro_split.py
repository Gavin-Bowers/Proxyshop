"""
* Templates: Retro Split and Room
"""
# Standard Library
from functools import cached_property
from typing import Optional, Union

# Third Party
from PIL import Image
# noinspection PyProtectedMember
from photoshop.api._artlayer import ArtLayer
# noinspection PyProtectedMember
from photoshop.api._layerSet import LayerSet
# noinspection PyProtectedMember
from photoshop.api import AnchorPosition

# Local
import src.helpers as psd

from src import CFG
from src.enums.layers import LAYERS
from src.enums.mtg import (MagicIcons, LayoutType)
from src.enums.settings import CollectorMode
from src.utils.adobe import LayerContainerTypes
from src.utils.adobe import ReferenceLayer

from src.text_layers import (
    ScaledTextField,
    FormattedTextArea,
    FormattedTextField,
    ScaledWidthTextField
)

from src.templates import RetroTemplate, SplitMod, contains_hybrid_mana

# region Data

# This doesn't include kewords for actions like Manifest Dread
KEYWORDS = \
["Eerie", "Battalion", "Bloodrush", "Channel", "Chroma", "Cohort", "Constellation",
"Converge", "Delirium", "Domain", "Fateful hour", "Ferocious", "Formidable", "Grandeur",
"Hellbent", "Heroic", "Imprint", "Inspired", "Join forces", "Kinship", "Landfall",
"Lieutenant", "Metalcraft", "Morbid", "Parley", "Radiance", "Raid", "Rally", "Spell mastery",
"Strive", "Sweep", "Tempting offer", "Threshold", "Will of the council", "Adamant",
"Addendum", "Council's dilemma", "Eminence", "Enrage", "Hero's Reward", "Kinfall",
"Landship", "Legacy", "Revolt", "Underdog", "Undergrowth", "Descend", "Fathomless descent",
"Magecraft", "Teamwork", "Pack tactics", "Coven", "Alliance", "Corrupted", "Secret council",
"Celebration", "Paradox", "Will of the Planeswalkers", "Survival", "Valiant",
"Start your engines!", "Living weapon", "Jump-start", "Commander ninjutsu",
"Legendary landwalk", "Nonbasic landwalk", "Megamorph", "Haunt", "Forecast", "Graft",
"Fortify", "Frenzy", "Gravestorm", "Hideaway", "Level Up", "Infect", "Reach", "Rampage",
"Phasing", "Multikicker", "Morph", "Provoke", "Modular", "Ninjutsu", "Replicate", "Recover",
"Poisonous", "Prowl", "Reinforce", "Persist", "Retrace", "Rebound", "Miracle", "Overload",
"Outlast", "Prowess", "Renown", "Myriad", "Shroud", "Trample", "Vigilance", "Storm",
"Soulshift", "Splice", "Transmute", "Ripple", "Suspend", "Vanishing", "Transfigure",
"Wither", "Undying", "Soulbond", "Unleash", "Ascend", "Assist", "Afterlife", "Companion",
"Fabricate", "Embalm", "Escape", "Fuse", "Menace", "Ingest", "Melee", "Improvise", "Mentor",
"Partner", "Mutate", "Tribute", "Surge", "Skulk", "Undaunted", "Riot", "Spectacle",
"Forestwalk", "Islandwalk", "Mountainwalk", "Double strike", "Cumulative upkeep",
"First strike", "Scavenge", "Encore", "Deathtouch", "Defender", "Amplify", "Affinity",
"Bushido", "Convoke", "Bloodthirst", "Absorb", "Aura Swap", "Changeling", "Conspire",
"Cascade", "Annihilator", "Battle Cry", "Cipher", "Bestow", "Dash", "Awaken", "Crew",
"Aftermath", "Afflict", "Flanking", "Foretell", "Fading", "Fear", "Eternalize", "Entwine",
"Epic", "Dredge", "Delve", "Evoke", "Exalted", "Evolve", "Extort", "Dethrone", "Exploit",
"Devoid", "Emerge", "Escalate", "Flying", "Haste", "Hexproof", "Indestructible",
"Intimidate", "Lifelink", "Horsemanship", "Kicker", "Madness", "Swampwalk", "Desertwalk",
"Craft", "Plainswalk", "Split second", "Augment", "Double agenda", "Reconfigure", "Ward",
"Partner with", "Daybound", "Nightbound", "Decayed", "Disturb", "Squad", "Enlist",
"Read Ahead", "Ravenous", "Blitz", "Offering", "Living metal", "Backup", "Banding",
"Hidden agenda", "For Mirrodin!", "Friends forever", "Casualty", "Protection",
"Compleated", "Devour", "Enchant", "Flash", "Boast", "Demonstrate", "Sunburst",
"Flashback", "Cycling", "Equip", "Buyback", "Hexproof from", "More Than Meets the Eye",
"Cleave", "Champion", "Specialize", "Training", "Prototype", "Toxic", "Unearth",
"Intensity", "Plainscycling", "Swampcycling", "Typecycling", "Wizardcycling",
"Mountaincycling", "Basic landcycling", "Islandcycling", "Forestcycling", "Slivercycling",
"Landcycling", "Bargain", "Choose a background", "Echo", "Disguise", "Doctor's companion",
"Landwalk", "Umbra armor", "Freerunning", "Spree", "Saddle", "Shadow", "Offspring",
"Impending", "Gift", "Exhaust"]

planeswalker_genders = {
    "Ajani": "masc",
    "Aminatou": "fem",
    "Angrath": "masc",
    "Arlinn": "fem",
    "Ashiok": "unknown",
    "Bahamut": "masc",
    "Basri": "masc",
    "Bolas": "masc",
    "Calix": "masc",
    "Chandra": "fem",
    "Comet": "masc",
    "Dack": "masc",
    "Dakkon": "masc",
    "Daretti": "masc",
    "Davriel": "masc",
    "Dihada": "fem",
    "Domri": "masc",
    "Dovin": "masc",
    "Ellywick": "fem",
    "Elminster": "masc",
    "Elspeth": "fem",
    "Estrid": "fem",
    "Freyalise": "fem",
    "Garruk": "masc",
    "Gideon": "masc",
    "Grist": "fem",
    "Guff": "masc",
    "Huatli": "fem",
    "Jace": "masc",
    "Jared": "masc",
    "Jaya": "fem",
    "Jeska": "fem",
    "Kaito": "masc",
    "Karn": "masc",
    "Kasmina": "fem",
    "Kaya": "fem",
    "Kiora": "fem",
    "Koth": "masc",
    "Liliana": "fem",
    "Lolth": "fem",
    "Lukka": "masc",
    "Minsc": "masc",
    "Mordenkainen": "masc",
    "Nahiri": "fem",
    "Narset": "fem",
    "Niko": "nonbinary",
    "Nissa": "fem",
    "Nixilis": "masc",
    "Oko": "masc",
    "Quintorius": "masc",
    "Ral": "masc",
    "Rowan": "fem",
    "Saheeli": "fem",
    "Samut": "fem",
    "Sarkhan": "masc",
    "Serra": "fem",
    "Sivitri": "fem",
    "Sorin": "masc",
    "Szat": "masc",
    "Tamiyo": "fem",
    "Tasha": "fem",
    "Teferi": "masc",
    "Teyo": "masc",
    "Tezzeret": "masc",
    "Tibalt": "masc",
    "Tyvar": "masc",
    "Ugin": "masc",
    "Urza": "masc",
    "Venser": "masc",
    "Vivien": "fem",
    "Vraska": "fem",
    "Vronos": "masc",
    "Will": "masc",
    "Windgrace": "masc",
    "Wrenn": "fem",
    "Xenagos": "masc",
    "Yanggu": "masc",
    "Yanling": "fem",
    "Zariel": "fem"
}

fade_mappings = {
    "WU": ("Left", "Right", "W", "U"),
    "WB": ("Left", "Right", "W", "B"),
    "RW": ("Right", "Left", "W", "R"),
    "GW": ("Right", "Left", "W", "G"),
    "UB": ("Left", "Right", "U", "B"),
    "UR": ("Left", "Right", "U", "R"),
    "GU": ("Right", "Left", "U", "G"),
    "BR": ("Left", "Right", "B", "R"),
    "BG": ("Left", "Right", "B", "G"),
    "RG": ("Left", "Right", "R", "G")
}

# This includes color orders which don't normally exist on cards
# Used for adventure card textboxes
extended_fade_mappings = {
    "WU": ("Left", "Right", "W", "U"),
    "WB": ("Left", "Right", "W", "B"),
    "RW": ("Right", "Left", "W", "R"),
    "GW": ("Right", "Left", "W", "G"),
    "UB": ("Left", "Right", "U", "B"),
    "UR": ("Left", "Right", "U", "R"),
    "GU": ("Right", "Left", "U", "G"),
    "BR": ("Left", "Right", "B", "R"),
    "BG": ("Left", "Right", "B", "G"),
    "RG": ("Left", "Right", "R", "G"),
    "UW": ("Right", "Left", "W", "U"),
    "BW": ("Right", "Left", "W", "B"),
    "WR": ("Left", "Right", "W", "R"),
    "WG": ("Left", "Right", "W", "G"),
    "BU": ("Right", "Left", "U", "B"),
    "RU": ("Right", "Left", "U", "R"),
    "UG": ("Left", "Right", "U", "G"),
    "RB": ("Right", "Left", "B", "R"),
    "GB": ("Right", "Left", "B", "G"),
    "GR": ("Right", "Left", "R", "G")
}

ordered_textbox_textures = [
    "Legends",
    "Land",
    "WL",
    "UL",
    "BL",
    "RL",
    "GL",
    "WL Dual",
    "UL Dual",
    "BL Dual",
    "RL Dual",
    "GL Dual",
    "W",
    "U",
    "B",
    "R",
    "G",
    "Gold",
    "Artifact",
    "Colorless"
]

ordered_frame_textures = [
    "W",
    "U",
    "B",
    "R",
    "G",
    "Gold",
    "Colorless",
    "Artifact",
    "Land",
    "Legends Land"
]

color_word_map = {
    "W": "white",
    "U": "blue",
    "B": "black",
    "R": "red",
    "G": "green",
    "C": "colorless"
}

# Color maps are for pinline colors

land_color_map = {
    'W': [217, 206, 200],
    'U': [12, 97, 122],
    'B': [76, 72, 71],
    'R': [199, 78, 49],  # Changed from CMM to 7ED for more saturation
    'G': [99, 142, 85],
    'Land': [244, 172, 38],
}

dual_land_color_map = {
    'W': [224, 217, 215],
    'U': [0, 119, 158],
    'B': [82, 81, 74],
    'R': [237, 97, 59],
    'G': [146, 192, 48],
    'Land': [244, 172, 38],
}

nonland_color_map = {
    'W': [217, 206, 200],
    'U': [12, 97, 122],
    'B': [76, 72, 71],
    'R': [198, 118, 89],
    'G': [99, 142, 85],
    'Gold': [184, 165, 110],
    'Artifact': [139, 124, 108],
    'Colorless': [198, 198, 198]
}

#endregion Data

# region Layer Visibility Functions

def set_layer_visibility(
    visible: bool,
    layer: ArtLayer | LayerSet | str,
    group: LayerContainerTypes | None = None,
):
    if layer is None: return

    if isinstance(layer, (ArtLayer, LayerSet)):
        layer.visible = visible
        return

    target: ArtLayer | LayerSet = psd.getLayerSet(layer, group)
    if target is None: # If a group is not found, look for a layer instead
        target = psd.getLayer(layer, group)

    # If neither are found, print an error and give up
    if target is None:
        print(f"Error: layer/group {layer} was not found in {group}")
        return

    target.visible = visible

def enable(
    layer: ArtLayer | LayerSet | str,
    group: LayerContainerTypes | None = None,
):
    set_layer_visibility(True, layer, group)

def disable(
    layer: ArtLayer | LayerSet | str,
    group: LayerContainerTypes | None = None,
):
    set_layer_visibility(False, layer, group)

# endregion

class RetroSplitTemplate(SplitMod, RetroTemplate):

    @cached_property
    def is_promo_star(self) -> bool:
        return CFG.get_setting(
            section='GENERAL',
            key='add_promo_star')

    @cached_property
    def is_align_collector_left(self) -> bool:
        return CFG.get_setting(
            section='GENERAL',
            key='align_collector_left')

    # region    Layers
    @cached_property
    def pinlines_layer(self) -> LayerSet:
        return psd.getLayerSet("Pinlines")

    @cached_property
    def card_frame_group(self) -> LayerSet:
        return psd.getLayerSet("Card Frame")

    @cached_property
    def art_frames_group(self) -> LayerSet:
        return psd.getLayerSet("Art Frames")

    @cached_property
    def art_pinlines_group(self) -> LayerSet:
        return psd.getLayerSet("Art", self.pinlines_layer)

    @cached_property
    def art_pinlines_masks_group(self) -> LayerSet:
        return psd.getLayerSet("Art Masks", self.pinlines_layer)

    @cached_property
    def art_pinlines_background_group(self) -> LayerSet:
        return psd.getLayerSet("Art Background", self.pinlines_layer)

    @cached_property
    def textbox_pinlines_group(self) -> LayerSet:
        return psd.getLayerSet("Textbox", self.pinlines_layer)

    @cached_property
    def textbox_pinlines_masks_group(self) -> LayerSet:
        return psd.getLayerSet("Textbox Masks", self.pinlines_layer)

    @cached_property
    def textbox_pinlines_background_group(self) -> LayerSet:
        return psd.getLayerSet("Textbox Background", self.pinlines_layer)

    @cached_property
    def outlines_group(self) -> LayerSet:
        return psd.getLayerSet("Outlines")

    @cached_property
    def art_outlines_group(self) -> LayerSet:
        return psd.getLayerSet("Art Outlines", self.outlines_group)

    @cached_property
    def textbox_outlines_group(self) -> LayerSet:
        return psd.getLayerSet("Textbox Outlines", self.outlines_group)

    @cached_property
    def textbox_bevels_group(self) -> LayerSet:
        return psd.getLayerSet("Textbox Bevels", self.card_frame_group)

    @cached_property
    def textbox_bevels_masks_group(self) -> LayerSet:
        return psd.getLayerSet("Masks", self.textbox_bevels_group)

    @cached_property
    def textbox_group(self) -> LayerSet:
        return psd.getLayerSet("Textbox", self.card_frame_group)

    @cached_property
    def textbox_masks_group(self) -> LayerSet:
        return psd.getLayerSet("Masks", self.textbox_group)

    @cached_property
    def textbox_effects_group(self) -> LayerSet:
        return psd.getLayerSet("Effects", self.textbox_group)

    @cached_property
    def bevels_group(self) -> LayerSet:
        return psd.getLayerSet("Bevels", self.card_frame_group)

    @cached_property
    def bevels_masks_group(self) -> LayerSet:
        return psd.getLayerSet("Masks", self.bevels_group)

    @cached_property
    def bevels_light_group(self) -> LayerSet:
        return psd.getLayerSet("Light", self.bevels_group)

    @cached_property
    def bevels_dark_group(self) -> LayerSet:
        return psd.getLayerSet("Dark", self.bevels_group)

    @cached_property
    def frame_texture_group(self) -> LayerSet:
        return psd.getLayerSet("Frame Texture", self.card_frame_group)

    @cached_property
    def frame_masks_group(self) -> LayerSet:
        return psd.getLayerSet("Masks", self.frame_texture_group)

    @cached_property
    def transform_group(self) -> LayerSet:
        return psd.getLayerSet(LAYERS.TRANSFORM, self.text_group)

    @cached_property
    def mdfc_group(self) -> LayerSet:
        return psd.getLayerSet("MDFC", self.text_group)

    @cached_property
    def mdfc_bottom_group(self) -> LayerSet:
        return psd.getLayerSet("Bottom", self.mdfc_group)

    @cached_property
    def adventure_group(self) -> LayerSet:
        return psd.getLayerSet("Adventure", self.text_group)
    # endregion

    # region    Text Layers
    @cached_property
    def text_layer_type(self) -> Optional[ArtLayer]:
        if not self.has_textbox:
            return None
        return psd.getLayer(LAYERS.TYPE_LINE, self.text_group)

    @cached_property
    def text_layer_name(self) -> ArtLayer:
        return psd.getLayer(LAYERS.NAME, self.text_group)

    @cached_property
    def text_layer_nickname(self) -> ArtLayer:
        return psd.getLayer("Nickname", self.text_group)

    @cached_property
    def text_layer_rules(self) -> ArtLayer:
        return psd.getLayer(LAYERS.RULES_TEXT, self.text_group)

    @cached_property
    def nickname_shape_layer(self) -> ArtLayer:
        return psd.getLayer("Nickname Box", self.text_group)

    # endregion

    # region    Properties

    @cached_property
    def pt_length(self) -> int:
        return len(f'{self.layout.power}{self.layout.toughness}')

    @cached_property
    def is_leveler(self) -> bool:
        return self.layout.card_class == LayoutType.Leveler

    @cached_property
    def is_prototype(self) -> bool:
        return self.layout.card_class == LayoutType.Prototype

    @cached_property
    def is_adventure(self) -> bool:
        return self.layout.card_class == LayoutType.Adventure

    @cached_property
    def is_mutate(self) -> bool:
        return self.layout.card_class == LayoutType.Mutate

    @cached_property
    def is_battle(self):
        return self.layout.card_class == LayoutType.Battle

    @cached_property
    def template_suffix(self) -> str:
        """Add Promo if promo star enabled."""
        return 'Promo' if self.is_promo_star else ''

    @cached_property
    def has_nickname(self) -> bool:
        """Return True if this a nickname render."""
        if self.flavor_name is not None:
            return True
        return False

    @cached_property
    def is_content_aware_enabled(self) -> bool:
        # if self.cfg_floating_frame:
        #     return True
        return False

    @cached_property
    def has_irregular_textbox(self) -> list[bool]:
        if self.is_saga or self.is_class:
            return False
        # if self.is_adventure:
        #     return False
        if (self.is_transform or self.is_mdfc) and self.cfg_has_tf_notch:
            return False
        if not self.cfg_irregular_textboxes:
            return False
        if self.has_pinlines:
            return False
        if self.identity_advanced == "G":
            return True
        if self.identity_advanced == "B":
            return True
        return False

    @cached_property
    def identity_advanced(self) -> str:
        if self.is_land:
            return LAYERS.LAND
        if self.is_split_fade:
            return LAYERS.HYBRID
        if self.is_artifact:
            return LAYERS.ARTIFACT
        if self.is_colorless:
            return LAYERS.COLORLESS
        if len(self.identity) > 1:
            return LAYERS.GOLD
        return self.identity

    @cached_property
    def has_pinlines(self) -> bool:
        if self.is_land:
            return True
        if len(self.identity) > 1 and self.cfg_pinlines_on_multicolored:
            return True
        if self.is_artifact and self.cfg_pinlines_on_artifacts:
            return True
        if self.cfg_pinlines_on_all_cards:
            return True
        return False

    @cached_property
    def has_textbox(self) -> bool:
        if self.textbox_size == "Textless":
            return False
        return True

    @cached_property
    def has_textbox_bevels(self) -> bool:
        if not self.has_textbox:
            return False
        if self.cfg_disable_textbox_bevels:
            return False
        if self.has_irregular_textbox:
            return False
        # if self.is_adventure:
        #     return False
        if self.is_land:
            if self.cfg_legends_style_lands:
                return False
            if self.is_gold_land:
                if self.cfg_textbox_bevels_on_gold_lands:
                    return True
                return False

        return True

    @cached_property
    def is_gold_land(self) -> bool:
        """ Whether the textbox of the card is the gold land textbox"""
        if not self.is_land:
            return False
        if self.is_basic_land:
            return False
        if self.cfg_gold_textbox_lands:
            return True
        if len(self.identity) < 1 or len(self.identity) > 2:
            return True
        return False

    @cached_property
    def is_dual_land(self) -> bool:
        if not self.is_land:
            return False
        if self.is_gold_land:
            return False
        if self.cfg_legends_style_lands:
            return False
        if len(self.identity) == 2:
            return True
        return False

    @cached_property
    def is_split_fade(self) -> bool:
        if len(self.identity) != 2:
            return False
        if self.cfg_split_all:
            return True
        if self.is_hybrid and self.cfg_split_hybrid:
            return True
        return False

    @cached_property
    def is_transparent(self) -> bool:
        if self.is_colorless and self.cfg_colorless_transparent:
            return True
        return False

    @cached_property
    def is_devoid(self) -> bool:
        # For some reason true colorless cards have "Colorless" as their color identity while
        # artifacts have an empty string.
        if self.identity == "Colorless":
            return False
        if self.is_colorless and (len(self.identity) > 0):
            return True
        return False

    @cached_property
    def is_saga(self) -> bool:
        return False

    @cached_property
    def is_class(self) -> bool:
        return False

    @cached_property
    def is_planeswalker(self) -> bool:
        return False

    @cached_property
    def is_normal(self) -> bool:
        if self.is_saga:
            return False
        if self.is_class:
            return False
        return True

    @cached_property
    def art_aspect(self) -> float:
        art_file = self.layout.art_file
        with Image.open(art_file) as img:
            width, height = img.size
            return width / height

    @cached_property
    def textbox_size_from_art_aspect(self) -> str:
        if self.art_aspect > 1.25:
            return "Normal"
        if self.art_aspect > 1.06:
            return "Medium"
        if self.art_aspect > 0.96:
            return "Small"
        return "Small"

    @cached_property
    def artref_size_from_art_aspect(self) -> str:
        """Currently same as the function above it, but may be changed"""
        if self.art_aspect > 1.25:
            return "Normal"
        if self.art_aspect > 1.06:
            return "Medium"
        if self.art_aspect > 0.96:
            return "Small"
        return "Small"

    @cached_property
    def textbox_size_from_text(self) -> str:
        """Returns an appropriate textbox size for the amount of text"""
        # Set up our test text layer
        test_layer = self.text_layer_rules
        test_text = self.layout.oracle_text
        if self.layout.flavor_text:
            test_text += f'\r{self.layout.flavor_text}'
        test_layer.textItem.contents = test_text.replace('\n', '\r')
        # Get the number of lines in our test text and decide what size
        num = psd.get_line_count(test_layer)
        if num < 5:
            return "Small"
        if num < 7:
            return "Medium"
        return "Normal"

    @cached_property
    def textbox_size(self) -> str:
        if self.is_room:
            return "Room"
        return "Normal"

    @cached_property
    def dual_fade_order(self) -> tuple[str, str, str, str] | None:
        """Returned values are: top mask, bottom mask, top layer identity, bottom layer identity"""
        return fade_mappings.get(self.identity)

    @cached_property
    def pinline_colors(self) -> dict:
        if self.is_land:
            if len(self.identity) == 2:
                return dual_land_color_map
            return land_color_map
        return nonland_color_map

    @cached_property
    def textbox_bevel_thickness(self) -> Optional[str]:
        if self.has_pinlines:
            return "Land"
        thickness_mappings = {
            "W": "Small",
            "U": "Large",
            "B": "Small",
            "R": "Large",
            "G": "Medium",
            "Gold": "Large",
            "Hybrid": "Medium",
            "Artifact": "Medium",
            "Colorless": "Medium"
        }
        return thickness_mappings.get(self.identity_advanced)

    @cached_property
    def is_centered(self) -> bool:
        """bool: Governs whether rules text is centered."""
        if self.is_adventure: return False
        return bool(
            len(self.layout.flavor_text) <= 1
            and len(self.layout.oracle_text) <= 70
            and "\n" not in self.layout.oracle_text)

    #endregion

    # region    Collector Info Methods
    # Copied from ClassicTemplate
    def process_layout_data(self) -> None:
        """Remove rarity letter from collector data."""
        super().process_layout_data()
        self.layout.collector_data = self.layout.collector_data[:-2] if (
                '/' in self.layout.collector_data
        ) else self.layout.collector_data[2:]

    def collector_info(self) -> None:
        """Format and add the collector info at the bottom."""

        # Which collector info mode?
        if CFG.collector_mode in [
            CollectorMode.Default, CollectorMode.Modern
        ] and self.layout.collector_data:
            layers = self.collector_info_authentic()
        elif CFG.collector_mode == CollectorMode.ArtistOnly:
            layers = self.collector_info_artist_only()
        else:
            layers = self.collector_info_basic()

        # Shift collector text
        if self.is_align_collector_left:
            [psd.align_left(n, ref=self.collector_reference.dims) for n in layers]

    # noinspection DuplicatedCode
    def collector_info_basic(self) -> list[ArtLayer]:
        """Called to generate basic collector info."""

        # Get artist and info layers
        artist = psd.getLayer(LAYERS.ARTIST, self.legal_group)
        info = psd.getLayer(LAYERS.SET, self.legal_group)

        # Fill optional promo star
        if self.is_collector_promo:
            psd.replace_text(info, "•", MagicIcons.COLLECTOR_STAR)

        # Apply the collector info
        if self.layout.lang != 'en':
            psd.replace_text(info, 'EN', self.layout.lang.upper())
        psd.replace_text(artist, "Artist", self.layout.artist)
        psd.replace_text(info, 'SET', self.layout.set)
        return [artist, info]

    # noinspection DuplicatedCode
    def collector_info_authentic(self) -> list[ArtLayer]:
        """Classic presents authentic collector info differently."""

        # Hide basic 'Set' layer
        psd.getLayer(LAYERS.SET, self.legal_group).visible = False

        # Get artist and info layers, reveal info layer
        artist = psd.getLayer(LAYERS.ARTIST, self.legal_group)
        info = psd.getLayer(LAYERS.COLLECTOR, self.legal_group)
        info.visible = True

        # Fill optional promo star
        if self.is_collector_promo:
            psd.replace_text(info, "•", MagicIcons.COLLECTOR_STAR)

        # Apply the collector info
        psd.replace_text(artist, 'Artist', self.layout.artist)
        psd.replace_text(info, 'SET', self.layout.set)
        psd.replace_text(info, 'NUM', self.layout.collector_data)
        return [artist, info]

    def collector_info_artist_only(self) -> list[ArtLayer]:
        """Called to generate 'Artist Only' collector info."""

        # Collector layers
        artist = psd.getLayer(LAYERS.ARTIST, self.legal_group)
        psd.getLayer(LAYERS.SET, self.legal_group).visible = False

        # Apply the collector info
        psd.replace_text(artist, "Artist", self.layout.artist)
        return [artist]
    # endregion

    # region    Layout logic
    @cached_property
    def flavor_name(self) -> Optional[str]:
        """Display name for nicknamed cards"""
        return self.layout.card.get('flavor_name')

    @cached_property
    def is_tombstone_scryfall(self) -> bool:
        return bool('tombstone' in self.layout.frame_effects)

    # Equivilent scryfall search:
    # o:"this card is in your graveyard" or o:"return this card from your graveyard" or o:"cast this card from your graveyard" or o:"put this card from your graveyard" or o:"exile this card from your graveyard" or o:"~ is in your graveyard" or o:"return ~ from your graveyard" or o:"cast ~ from your graveyard" or o:"put ~ from your graveyard" or o:"exile ~ from your graveyard" or keyword:disturb or keyword:flashback or keyword:Dredge or keyword:Scavenge or keyword:Embalm or keyword:Eternalize or keyword:Aftermath or keyword:Encore or keyword:Escape or keyword:Jump-start or keyword:Recover or keyword:Retrace or keyword:Unearth
    # (Excluding named cards)

    @cached_property
    def is_tombstone_auto(self) -> bool:
        keyword_list = [
            'Flashback',
            'Dredge',
            'Scavenge',
            'Embalm',
            'Eternalize',
            'Aftermath',
            'Disturb',
            'Encore',
            'Escape',
            'Jump-start',
            'Recover',
            'Retrace',
            'Unearth',
        ]
        for keyword in keyword_list:
            if keyword in self.layout.keywords: return True

        cardname = self.layout.name_raw.lower()
        oracle_text = self.layout.oracle_text.lower()

        key_phrase_list = [
            f'{cardname} is in your graveyard',
            f'return {cardname} from your graveyard',
            f'cast {cardname} from your graveyard',
            f'put {cardname} from your graveyard',
            f'exile {cardname} from your graveyard',
        ]
        for phrase in key_phrase_list:
            if phrase in oracle_text: return True

        key_phrase_list_generic = [
            f'this card is in your graveyard',
            f'return this card from your graveyard',
            f'cast this card from your graveyard',
            f'put this card from your graveyard',
            f'exile this card from your graveyard',
        ]
        for phrase in key_phrase_list_generic:
            if phrase in oracle_text: return True

        name_list = [
            "Say Its Name",
            "Skyblade's Boon",
            "Nether Spirit",
        ]
        for name in name_list:
            if name == self.layout.name_raw: return True
        return False

    @cached_property
    def has_tombstone(self) -> bool:
        setting = self.cfg_tombstone_setting
        match setting:
            case "Automatic":
                return self.is_tombstone_auto
            case "Scryfall":
                return self.is_tombstone_scryfall
        return False
    # endregion

    # region    Layer logic
    @cached_property
    def frame_texture(self) -> ArtLayer:
        if self.is_land and self.cfg_legends_style_lands:
            return psd.getLayer("Legends Land", self.frame_texture_group)
        return psd.getLayer(self.identity_advanced, self.frame_texture_group)

    @cached_property
    def frame_mask(self) -> ArtLayer:
        return psd.getLayer(self.textbox_size, self.frame_masks_group)

    @cached_property
    def textbox_textures(self) -> list[ArtLayer]: #TODO
        if self.is_land:
            if self.cfg_legends_style_lands:
                return psd.getLayer("Legends", self.textbox_group)
            if self.is_gold_land:
                return psd.getLayer("Land", self.textbox_group)
            return psd.getLayer(self.identity + "L", self.textbox_group)
        return psd.getLayer(self.identity_advanced, self.textbox_group)

    @cached_property
    def textbox_shapes(self) -> list[Optional[ArtLayer]]:
        res = []
        for group in self.textbox_masks_groups:
            if self.textbox_size == "Textless":
                res += None
            elif self.has_irregular_textbox:
                res += psd.getLayer(f"{self.identity_advanced} {self.textbox_size}", group)
            else:
                res += psd.getLayer(self.textbox_size, group)
        return res

    @cached_property
    def art_references(self) -> list[ReferenceLayer]:
        res = []
        for group in self.art_frames_groups:
            if self.is_transparent:
                res += psd.get_reference_layer("Transparent Frame", group)
            else:
                res += psd.get_reference_layer(self.textbox_size, group)
        return res

    @cached_property
    def textbox_references(self) -> list[ReferenceLayer]:
        return [psd.get_reference_layer(f"Textbox Reference {self.textbox_size}", group)
                for group in self.text_groups]

    @cached_property
    def collector_references(self) -> list[ReferenceLayer]:
        return [psd.get_reference_layer(LAYERS.COLLECTOR_REFERENCE, group) for group in self.legal_groups]

    @cached_property
    def expansion_references(self) -> list[ReferenceLayer]:
        return [psd.get_reference_layer("Expansion Reference", group) for group in self.text_groups]

    @cached_property
    def art_outlines(self) -> list[LayerSet]:
        return [psd.getLayerSet(self.textbox_size, group) for group in self.art_outlines_groups]

    @cached_property
    def textbox_outlines(self) -> list[Optional[ArtLayer]]:
        res = []
        for textbox in self.has_irregular_textbox:
            if textbox:
                res += None
            else:
                res += psd.getLayer(self.textbox_size, self.textbox_outlines_group)
        return res

    # endregion

    # region    Text Functions

    # No nickname support on split cards
    # There are no existing split cards with nicknames and I imagine it'll stay that way

    def adjust_mana_cost(self): # DONE
        """Adjusts the size and position of the mana cost depending
        on if hybrid symbols are present and whether pinlines are enabled"""

        for i in range(2):
            if contains_hybrid_mana(self.layout.mana_cost[i]):
                if self.has_pinlines[i]:
                    psd.set_text_size(self.text_layer_mana[i], 4.5)
                    self.text_layer_mana[i].translate(0, -7.5)
                else:
                    self.text_layer_mana[i].translate(0, -6)
            elif self.has_pinlines[i]:
                self.text_layer_mana[i].translate(0,-1.5)

    # endregion

    # region    Layer adding functions
    def load_expansion_symbol(self) -> None:
        """Import and loads the expansion symbol, except on textless cards"""
        if not self.has_textbox:
            return
        super().load_expansion_symbol()

    @cached_property
    def textbox_pinlines_colors(self) -> Union[list[int], list[dict]]:
        if self.is_land:
            if (not self.is_basic_land and self.cfg_gold_textbox_lands) or (len(self.identity) > self.cfg_max_pinline_colors):
                return psd.get_pinline_gradient("Land", color_map=self.pinline_colors)
        return psd.get_pinline_gradient(
            self.identity if 1 < len(self.identity) <= self.cfg_max_pinline_colors else self.pinlines,
            color_map=self.pinline_colors)

    @cached_property
    def non_textbox_pinlines_colors(self) -> Union[list[int], list[dict]]:
        """Must be returned as SolidColor or gradient notation."""
        if not self.cfg_color_all_pinlines:
            if self.is_land and not self.is_basic_land:
                return psd.get_pinline_gradient("Land", color_map=self.pinline_colors)
            if len(self.identity) > 1:
                if self.is_artifact:
                    return psd.get_pinline_gradient("Artifact", color_map=self.pinline_colors)
                if self.is_colorless:
                    return psd.get_pinline_gradient("Colorless", color_map=self.pinline_colors)
                return psd.get_pinline_gradient("Gold", color_map=self.pinline_colors)
        return self.textbox_pinlines_colors

    def add_pinlines(self):
        enable(self.pinlines_layer)
        enable(self.textbox_size, self.art_pinlines_background_group)

        if self.cfg_legends_style_lands and self.is_land:
            enable(f"Legends {self.textbox_size}", psd.getLayerSet("Legends", self.pinlines_layer))

        self.generate_layer(group=psd.getLayerSet("Outer", self.pinlines_layer),
                            colors=self.non_textbox_pinlines_colors)

        self.generate_layer(group=psd.getLayerSet("Art", self.pinlines_layer), colors=self.non_textbox_pinlines_colors)
        art_mask = psd.getLayer(self.textbox_size, self.art_pinlines_masks_group)
        psd.copy_vector_mask(art_mask, self.art_pinlines_group)

        if not self.has_textbox: return

        enable(self.textbox_size, self.textbox_pinlines_background_group)
        self.generate_layer(group=psd.getLayerSet("Textbox", self.pinlines_layer), colors=self.textbox_pinlines_colors)
        textbox_mask = psd.getLayer(self.textbox_size, self.textbox_pinlines_masks_group)
        psd.copy_vector_mask(textbox_mask, self.textbox_pinlines_group)

    def add_outer_and_art_bevels(self):
        light_mask = psd.getLayer(self.textbox_size + " Light", self.bevels_masks_group)
        dark_mask = psd.getLayer(self.textbox_size + " Dark", self.bevels_masks_group)

        for (mask, layer) in [
            (light_mask, self.bevels_light_group),
            (dark_mask, self.bevels_dark_group)
        ]:
            psd.copy_vector_mask(mask, layer)
            enable(self.identity_advanced, layer)

    def add_textbox_bevels(self, identity=None):
        if not self.has_textbox_bevels: return

        if identity is None:
            identity = self.identity_advanced

        tr, bl, textbox_bevel = self.copy_textbox_bevel_masks(identity)

        # Enables lines which exist on white, blue, and red textbox bevels
        # They don't look good on hybrid cards, and I haven't implemented
        # The right size and placements for cards with pinlines
        if self.is_split_fade: return
        if self.has_pinlines: return
        if identity == "W" or identity == "U" or identity == "R":
            enable(self.textbox_size, textbox_bevel)

    def copy_textbox_bevel_masks(self, identity) -> tuple[LayerSet, LayerSet, LayerSet]:
        sized_bevel_masks = psd.getLayerSet(self.textbox_size, self.textbox_bevels_masks_group)
        textbox_bevel = psd.getLayerSet(identity, self.textbox_bevels_group)

        enable(textbox_bevel)

        (top_right, bottom_left) = \
            (psd.getLayerSet("TR", textbox_bevel), psd.getLayerSet("BL", textbox_bevel))

        top_right_mask = psd.getLayer(self.textbox_bevel_thickness + " TR", sized_bevel_masks)
        bottom_left_mask = psd.getLayer(self.textbox_bevel_thickness + " BL", sized_bevel_masks)

        psd.copy_vector_mask(top_right_mask, top_right)
        psd.copy_vector_mask(bottom_left_mask, bottom_left)

        return top_right, bottom_left, textbox_bevel

    def dual_fade_frame_texture(self):
        (top_mask_name, _, top_layer, bottom_layer) = self.dual_fade_order

        top_mask = psd.getLayer(top_mask_name, LAYERS.MASKS)
        top_frame_layer = psd.getLayer(top_layer, self.frame_texture_group)
        bottom_frame_layer = psd.getLayer(bottom_layer, self.frame_texture_group)

        psd.copy_layer_mask(top_mask, top_frame_layer)

        enable(top_frame_layer)
        enable(bottom_frame_layer)

    def dual_fade_nonland_textbox(self, colors_override = None):
        color_source = self.dual_fade_order if colors_override is None else colors_override
        (top_mask_name, _, top_layer, bottom_layer) = color_source

        top_mask = psd.getLayer(top_mask_name, LAYERS.MASKS)
        top_textbox_layer = psd.getLayer(top_layer, self.textbox_group)
        bottom_textbox_layer = psd.getLayer(bottom_layer, self.textbox_group)

        psd.copy_layer_mask(top_mask, top_textbox_layer)

        enable(top_textbox_layer)
        enable(bottom_textbox_layer)

    def dual_fade_textbox_bevels(self):
        if not self.has_textbox_bevels: return

        (top_mask_name, bottom_mask_name, top_layer, bottom_layer) = self.dual_fade_order

        top_mask = psd.getLayer(top_mask_name, LAYERS.MASKS)
        bottom_mask = psd.getLayer(bottom_mask_name, LAYERS.MASKS)

        for mask_layer, layer in [
            (top_mask, top_layer),
            (bottom_mask, bottom_layer),
        ]:
            self.add_textbox_bevels(identity=layer)
            psd.copy_layer_mask(mask_layer, psd.getLayerSet(layer, self.textbox_bevels_group))

    def dual_fade_bevels(self):

        (top_mask_name, bottom_mask_name, top_layer, bottom_layer) = self.dual_fade_order

        top_mask = psd.getLayer(top_mask_name, LAYERS.MASKS)
        bottom_mask = psd.getLayer(bottom_mask_name, LAYERS.MASKS)
        light_mask = psd.getLayer(self.textbox_size + " Light", self.bevels_masks_group)
        dark_mask = psd.getLayer(self.textbox_size + " Dark", self.bevels_masks_group)

        psd.copy_vector_mask(light_mask, self.bevels_light_group)
        psd.copy_vector_mask(dark_mask, self.bevels_dark_group)

        for (mask, layer, group) in [
            (top_mask, top_layer, self.bevels_light_group),
            (top_mask, top_layer, self.bevels_dark_group),
            (bottom_mask, bottom_layer, self.bevels_light_group),
            (bottom_mask, bottom_layer, self.bevels_dark_group),
        ]:
            enable(layer, group)
            psd.copy_layer_mask(mask, psd.getLayer(layer, group))

    def position_type_line(self):
        """Positions the type line elements vertically based on the textbox size"""
        if not self.has_textbox: return

        match self.textbox_size:
            case "Medium":
                offset = 220
            case "Small":
                offset = 365
            case "Saga":
                offset = 587
            case "Class":
                offset = 587
            case _:
                offset = 0

        if self.has_pinlines:
            if self.expansion_symbol_layer:
                self.expansion_symbol_layer.resize(90, 90, AnchorPosition.MiddleCenter)
            offset += 4

        self.text_layer_type.translate(0, offset)
        if self.expansion_symbol_layer:
            self.expansion_symbol_layer.translate(0, offset)
        if self.color_indicator_layer:
            self.color_indicator_layer.translate(0, offset)

        if self.is_type_shifted:
            self.text_layer_type.translate(100, 0)

    def add_tombstone(self):
        # Enables smaller tombstone icon which sits below the transform icon
        if self.is_transform and self.is_front:
            icon_name = "Tombstone Small"
        else:
            icon_name = "Tombstone"

        enable(icon_name, self.text_group)

    def add_textbox_notch(self):
        cardtype = ""
        if self.is_mdfc:
            cardtype = "MDFC"
        if self.is_transform:
            cardtype = "TF"

        enable(f"{cardtype} Notch", self.textbox_masks_group)
        psd.copy_vector_mask(psd.getLayer(f"Textbox Outlines {cardtype}", self.mask_group), self.textbox_outlines_group)

        bevel_overlays = psd.getLayerSet(f"Textbox Bevel Overlays {cardtype}", self.card_frame_group)

        if self.has_textbox_bevels:
            color = self.identity_advanced

            if self.is_split_fade:
                color = "Hybrid"

            enable(color, bevel_overlays)
            psd.copy_vector_mask(psd.getLayer(f"Textbox Bevels {cardtype}", self.mask_group), self.textbox_bevels_group)

            if self.is_land:
                color = self.identity
                if len(color) > 2: color = "Gold"

                if self.is_dual_land:
                    (top, _, top_color, bottom_color) = self.dual_fade_order
                    notch_side = "Left" if cardtype == "MDFC" else "Right"
                    color = top_color if notch_side == top else bottom_color

                print(color)
                land_bevel_overlays = psd.getLayerSet("Land", bevel_overlays)
                enable(color, psd.getLayerSet("TR", land_bevel_overlays))
                enable(color, psd.getLayerSet("BL", land_bevel_overlays))

        if self.has_pinlines:
            enable("Pinlines", bevel_overlays)
            psd.copy_vector_mask(psd.getLayer(f"Pinlines {cardtype}", self.mask_group), self.pinlines_layer)
            self.generate_layer(
                group=psd.getLayerSet("Pinlines", psd.getLayerSet("Pinlines", bevel_overlays)),
                colors=self.textbox_pinlines_colors
            )
        else:
            enable(f"{cardtype} Notch", self.outlines_group)

    def add_nonland_frame_texture(self):
        if self.is_split_fade:
            self.dual_fade_frame_texture()
            self.dual_fade_bevels()
        # elif self.is_adventure and self.has_different_adventure_color:
        #     mask, layer, _, _ = self.adventure_mask_info
        #
        #     psd.copy_vector_mask(
        #         psd.getLayer(f"Adventure Frame{mask}", self.mask_group),
        #         psd.getLayer(layer, self.frame_texture_group))
        #
        #     enable(self.layout.adventure_colors, self.frame_texture_group)
        #     enable(self.identity_advanced, self.frame_texture_group)
        #     self.add_outer_and_art_bevels()
        else:
            enable(self.frame_texture)
            self.add_outer_and_art_bevels()

    def add_nonland_textbox(self):
        if self.is_split_fade:
            self.dual_fade_nonland_textbox()
            if self.cfg_dual_textbox_bevels:
                self.dual_fade_textbox_bevels()
            else:
                self.add_textbox_bevels()

        # elif self.is_adventure and self.has_different_adventure_color:
        #
        #     mask, top_layer, _, _ = self.adventure_mask_info
        #
        #     psd.copy_vector_mask(
        #         psd.getLayer(f"Adventure Textbox{mask}", self.mask_group),
        #         psd.getLayer(top_layer, self.textbox_group))
        #
        #     enable(self.layout.adventure_colors, self.textbox_group)
        #     enable(self.identity_advanced, self.textbox_group)
        #
            #self.dual_fade_nonland_textbox(colors_override=self.dual_fade_order_adventure)
            #self.add_textbox_bevels()
        else:
            enable(self.textbox_texture)
            self.add_textbox_bevels()

    def apply_textbox_shape(self):
        if not (self.identity_advanced == "B" and self.is_normal and self.has_irregular_textbox):
            # Enables vector mask for vectorized textboxes (including green)
            enable(self.textbox_shape)
        else:
            # Enables rasterized textbox for black textboxes
            enable(f"B {self.textbox_size}", self.textbox_group)

    def apply_devoid(self):
        color = self.identity if len(self.identity) == 1 else "Gold"
        color_layer = psd.getLayer(color, self.frame_texture_group)
        enable(color_layer.visible)
        psd.copy_layer_mask(psd.getLayer("Devoid Color", self.mask_group), color_layer)

        if self.is_transparent:
            psd.copy_layer_mask(psd.getLayer("Devoid", self.mask_group), self.card_frame_group)

        if self.cfg_colored_bevels_on_devoid:
            enable(color, self.bevels_light_group)
            enable(color, self.bevels_dark_group)

            psd.copy_layer_mask(
                psd.getLayer("Devoid Color", self.mask_group),
                psd.getLayer(color, self.bevels_light_group))

            psd.copy_layer_mask(
                psd.getLayer("Devoid Color", self.mask_group),
                psd.getLayer(color, self.bevels_dark_group))

    def add_outlines(self):
        enable(self.art_outlines)
        if self.textbox_outlines is not None:
            enable(self.textbox_outlines)

    def add_nickname_plate(self):
        enable("Nickname", self.text_group)
        enable("Nickname Box", self.text_group)

        masks = psd.getLayerSet("Masks", self.frame_texture_group)
        enable("Nickname", masks)

        nickname_mask = psd.getLayer("Nickname", self.mask_group)
        psd.copy_vector_mask(nickname_mask, self.outlines_group)
        psd.copy_vector_mask(nickname_mask, self.bevels_group)

    def add_textbox_decorations(self):
        """Adds the color indicator and fx to textboxes when appropriate"""
        if self.is_type_shifted and self.color_indicator_layer:
            enable(self.color_indicator_layer)

        # Applies dropshadow effect to green textbox
        if self.identity_advanced == "G":
            psd.copy_layer_fx(psd.getLayer("G", self.textbox_effects_group), self.textbox_group)

    def add_textbox(self):
        if self.is_land: self.add_land_textbox()
        if not self.is_land: self.add_nonland_textbox()
        self.apply_textbox_shape()
        self.add_textbox_decorations()

    def enable_frame_layers(self):
        enable(self.frame_mask)
        self.add_outlines()

        if self.is_land: self.add_land_frame_texture()
        if not self.is_land: self.add_nonland_frame_texture()

        if self.cfg_floating_frame: disable(self.border_group)
        if self.is_devoid: self.apply_devoid()
        if self.has_textbox:
            self.add_textbox()
            self.position_type_line()
        # if not self.has_textbox: disable(self.expansion_symbol_layer)
        if self.has_pinlines: self.add_pinlines()
        if self.has_nickname: self.add_nickname_plate()
        if self.is_promo_star: enable("Promo Star", self.text_group)
        if self.has_tombstone: self.add_tombstone()
        #if self.is_adventure: enable(self.adventure_group)
    # endregion