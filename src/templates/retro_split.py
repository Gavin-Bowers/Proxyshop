"""
* Templates: Retro Split and Room
"""
# Standard Library
from functools import cached_property
from typing import Optional

# Third Party
# noinspection PyProtectedMember
from photoshop.api._artlayer import ArtLayer
# noinspection PyProtectedMember
from photoshop.api._layerSet import LayerSet

# Local
import src.helpers as psd
from src import CFG
from src.enums.layers import LAYERS
from src.enums.mtg import (MagicIcons)
from src.enums.settings import CollectorMode
from src.templates import RetroTemplate, SplitMod, contains_hybrid_mana
from src.text_layers import FormattedTextArea
from src.utils.adobe import LayerContainerTypes
from src.utils.adobe import ReferenceLayer

# region Data

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
        print(f"Error: layer {layer} was not found")
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

    # region    Layers

    @cached_property
    def sides(self) -> list[LayerSet]:
        return [psd.getLayerSet("Left"), psd.getLayerSet("Right")]

    @cached_property
    def mask_groups(self) -> list[LayerSet]:
        return [psd.getLayerSet(LAYERS.MASKS, side) for side in self.sides]

    @cached_property
    def card_frame_groups(self) -> list[LayerSet]:
        return [psd.getLayerSet("Card Frame", side) for side in self.sides]

    @cached_property
    def art_frames_groups(self) -> list[LayerSet]:
        return [psd.getLayerSet("Art Frames", side) for side in self.sides]

    @cached_property
    def outlines_groups(self) -> list[LayerSet]:
        return [psd.getLayerSet("Outlines", side) for side in self.sides]

    @cached_property
    def art_outlines_groups(self) -> list[LayerSet]:
        return [psd.getLayerSet("Art Outlines", self.outlines_groups[i]) for i in range(2)]

    @cached_property
    def textbox_outlines_groups(self) -> list[LayerSet]:
        return [psd.getLayerSet("Textbox Outlines", self.outlines_groups[i]) for i in range(2)]

    @cached_property
    def textbox_bevels_groups(self) -> list[LayerSet]:
        return [psd.getLayerSet("Textbox Bevels", self.card_frame_groups[i]) for i in range(2)]

    @cached_property
    def textbox_bevels_mask_groups(self) -> list[LayerSet]:
        return [psd.getLayerSet("Masks", self.textbox_bevels_groups[i]) for i in range(2)]

    @cached_property
    def textbox_groups(self) -> list[LayerSet]:
        return [psd.getLayerSet("Textbox", self.card_frame_groups[i]) for i in range(2)]

    @cached_property
    def textbox_mask_groups(self) -> list[LayerSet]:
        return [psd.getLayerSet("Masks", self.textbox_groups[i]) for i in range(2)]

    @cached_property
    def textbox_effects_groups(self) -> list[LayerSet]:
        return [psd.getLayerSet("Effects", self.textbox_groups[i]) for i in range(2)]

    @cached_property
    def bevels_groups(self) -> list[LayerSet]:
        return [psd.getLayerSet("Bevels", self.card_frame_groups[i]) for i in range(2)]

    @cached_property
    def bevels_mask_groups(self) -> list[LayerSet]:
        return [psd.getLayerSet("Masks", self.bevels_groups[i]) for i in range(2)]

    @cached_property
    def bevels_light_groups(self) -> list[LayerSet]:
        return [psd.getLayerSet("Light", self.bevels_groups[i]) for i in range(2)]

    @cached_property
    def bevels_dark_groups(self) -> list[LayerSet]:
        return [psd.getLayerSet("Dark", self.bevels_groups[i]) for i in range(2)]

    @cached_property
    def frame_texture_groups(self) -> list[LayerSet]:
        return [psd.getLayerSet("Frame Texture", self.card_frame_groups[i]) for i in range(2)]

    @cached_property
    def frame_mask_groups(self) -> list[LayerSet]:
        return [psd.getLayerSet("Masks", self.frame_texture_groups[i]) for i in range(2)]

    @cached_property
    def expansion_reference(self) -> ArtLayer:
        return psd.getLayer(LAYERS.EXPANSION_REFERENCE, self.text_groups[0])

    @cached_property
    def expansion_reference_right(self) -> ArtLayer:
        return psd.getLayer(LAYERS.EXPANSION_REFERENCE, self.text_groups[1])

    # endregion

    # region    Text Layers

    @cached_property
    def text_groups(self) -> list[LayerSet]:
        return [psd.getLayerSet(LAYERS.TEXT_AND_ICONS, side) for side in self.sides]

    @cached_property
    def text_layer_type(self) -> list[ArtLayer]:
        return [psd.getLayer(LAYERS.TYPE_LINE, self.text_groups[i]) for i in range(2)]

    @cached_property
    def text_layer_name(self) -> list[ArtLayer]:
        return [psd.getLayer(LAYERS.NAME, self.text_groups[i]) for i in range(2)]

    @cached_property
    def text_layers_rules(self) -> list[ArtLayer]:
        return [psd.getLayer(LAYERS.RULES_TEXT, self.text_groups[i]) for i in range(2)]

    @cached_property
    def oracle_text_with_fuse(self) -> list[str]:
        """Both side oracle texts. This version keeps fuse in the oracle text"""
        text = []
        for t in [
            c.get('printed_text', c.get('oracle_text', ''))
            if self.layout.is_alt_lang else c.get('oracle_text', '')
            for c in self.layout.card
        ]:
            text.append(t)
        return text

    def rules_text_and_pt_layers(self) -> None:
        """Add rules and P/T text for each face."""
        for i in range(2):
            self.text.append(
                FormattedTextArea(
                    layer=self.text_layer_rules[i],
                    contents=self.oracle_text_with_fuse[i],
                    flavor=self.layout.flavor_text[i],
                    reference=self.textbox_reference[i],
                    divider=self.divider_layer[i],
                    centered=self.is_centered[i]))

    # endregion

    # region    Properties

    @cached_property
    def is_content_aware_enabled(self) -> bool:
        return False

    @cached_property
    def has_textbox(self) -> bool:
        return True

    @cached_property
    def textbox_size(self) -> str:
        # if self.is_room:
        #     return "Room"
        return "Normal"

    @cached_property
    def has_irregular_textbox(self) -> list[bool]:
        res = []
        for i in range(2):
            if not self.cfg_irregular_textboxes:
                res.append(False)
            elif self.identity_advanced[i] == "G" or self.identity_advanced[i] == "B":
                res.append(True)
            else:
                res.append(False)
        return res

    @cached_property
    def has_textbox_bevels(self) -> list[bool]:
        res = []
        for i in range(2):
            if self.cfg_disable_textbox_bevels:
                res.append(False)
            elif self.has_irregular_textbox[i]:
                res.append(False)
            else:
                res.append(True)
        return res

    @cached_property
    def textbox_bevel_thickness(self) -> list[str]:
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
        return [thickness_mappings.get(self.identity_advanced[i]) for i in range(2)]

    @cached_property
    def identity_advanced(self) -> list[str]:
        res = []
        for i in range(2):
            if self.is_split_fade[i]:
                res.append(LAYERS.HYBRID)
            elif len(self.layout.identity[i]) > 1:
                res.append(LAYERS.GOLD)
            else:
                res.append(self.layout.identity[i])
        return res

    @cached_property
    def is_split_fade(self) -> list[bool]:
        res = []
        for i in range(2):
            if len(self.layout.identity[i]) != 2:
                res.append(False)
            elif self.cfg_split_all:
                res.append(True)
            elif self.layout.is_hybrid[i] and self.cfg_split_hybrid:
                res.append(True)
            else:
                res.append(False)
        return res

    @cached_property
    def dual_fade_order(self) -> list[tuple[str, str, str, str] | None]:
        """Returned values are: top mask, bottom mask, top layer identity, bottom layer identity"""
        return [fade_mappings.get(self.layout.identity[i]) for i in range(2)]

    #endregion

    # region    Collector Info Methods

    @cached_property
    def legal_groups(self) -> list[LayerSet]:
        """LayerSet: Group containing artist credit, collector info, and other legal details."""
        return [psd.getLayerSet(LAYERS.LEGAL, side) for side in self.sides]

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
            layers = self.collector_infos_authentic()
        elif CFG.collector_mode == CollectorMode.ArtistOnly:
            layers = self.collector_infos_artist_only()
        else:
            layers = self.collector_infos_basic()

        # Shift collector text
        if self.is_align_collector_left:
            [psd.align_left(n, ref=self.collector_reference.dims) for n in layers]

    def collector_infos_basic(self) -> list[ArtLayer]:
        # Nested list comprehension results in single list with all artlLayers
        return [item for i in range(2) for item in self.collector_info_basic_side(i)]

    def collector_info_basic_side(self, side) -> list[ArtLayer]:
        """Called to generate basic collector info."""

        # Get artist and info layers
        artist = psd.getLayer(LAYERS.ARTIST, self.legal_groups[side])
        info = psd.getLayer(LAYERS.SET, self.legal_groups[side])

        # Fill optional promo star
        if self.is_collector_promo:
            psd.replace_text(info, "•", MagicIcons.COLLECTOR_STAR)

        # Apply the collector info
        if self.layout.lang != 'en':
            psd.replace_text(info, 'EN', self.layout.lang.upper())
        psd.replace_text(artist, "Artist", self.layout.artists[side])
        psd.replace_text(info, 'SET', self.layout.set)
        return [artist, info]

    def collector_infos_authentic(self) -> list[ArtLayer]:
        return [item for i in range(2) for item in self.collector_info_authentic_side(i)]

    def collector_info_authentic_side(self, side) -> list[ArtLayer]:
        """Classic presents authentic collector info differently."""

        # Hide basic 'Set' layer
        psd.getLayer(LAYERS.SET, self.legal_groups[side]).visible = False

        # Get artist and info layers, reveal info layer
        artist = psd.getLayer(LAYERS.ARTIST, self.legal_groups[side])
        info = psd.getLayer(LAYERS.COLLECTOR, self.legal_groups[side])
        info.visible = True

        # Fill optional promo star
        if self.is_collector_promo:
            psd.replace_text(info, "•", MagicIcons.COLLECTOR_STAR)

        # Apply the collector info
        psd.replace_text(artist, 'Artist', self.layout.artists[side])
        psd.replace_text(info, 'SET', self.layout.set)
        psd.replace_text(info, 'NUM', self.layout.collector_data)
        return [artist, info]

    def collector_infos_artist_only(self) -> list[ArtLayer]:
        return [item for i in range(2) for item in self.collector_info_artist_only_side(i)]

    def collector_info_artist_only_side(self, side) -> list[ArtLayer]:
        """Called to generate 'Artist Only' collector info."""

        # Collector layers
        artist = psd.getLayer(LAYERS.ARTIST, self.legal_groups[side])
        psd.getLayer(LAYERS.SET, self.legal_groups[side]).visible = False

        # Apply the collector info
        psd.replace_text(artist, "Artist", self.layout.artists[side])
        return [artist]
    # endregion

    # region    Layout logic

    # The only split cards with tombstones are Aftermath cards
    @cached_property
    def is_aftermath(self) -> bool:
        if "Aftermath" in self.layout.keywords:
            return True
        return False

    @cached_property
    def is_room(self) -> bool:
        if "Room" in self.layout.type_line[0]:
            return True
        return False
    # endregion

    # region    Layer logic
    @cached_property
    def frame_textures(self) -> list[ArtLayer]:
        return [psd.getLayer(self.identity_advanced[i], self.frame_texture_groups[i]) for i in range(2)]

    @cached_property
    def frame_masks(self) -> list[ArtLayer]:
        return [psd.getLayer(self.textbox_size, self.frame_mask_groups[i]) for i in range(2)]

    @cached_property
    def textbox_textures(self) -> list[ArtLayer]:
        return [psd.getLayer(self.identity_advanced[i], self.textbox_groups[i]) for i in range(2)]

    @cached_property
    def textbox_shapes(self) -> list[ArtLayer]:
        res = []
        for i in range(2):
            if self.has_irregular_textbox[i]:
                res.append(psd.getLayer(f"{self.identity_advanced[i]} {self.textbox_size}", self.textbox_mask_groups[i]))
            else:
                res.append(psd.getLayer(self.textbox_size, self.textbox_mask_groups[i]))
        return res

    @cached_property
    def art_references(self) -> list[ReferenceLayer]:
        return [psd.get_reference_layer(self.textbox_size, self.art_frames_groups[i]) for i in range(2)]

    @cached_property
    def art_reference(self) -> list[ArtLayer]:
        """Art layer positioning reference for each side."""
        return [psd.getLayer(self.textbox_size, self.art_frames_groups[i]) for i in range(2)]

    @cached_property
    def textbox_reference(self) -> list[ReferenceLayer]:
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
        for i in range(2):
            if self.has_irregular_textbox[i]:
                res.append(None)
            else:
                res.append(psd.getLayer(self.textbox_size, self.textbox_outlines_groups[i]))
        return res

    def adjust_mana_cost(self):
        """Adjusts the size and position of the mana cost depending on if hybrid symbols are present"""
        for i in range(2):
            if contains_hybrid_mana(self.layout.mana_cost[i]):
                self.text_layer_mana[i].translate(0, -6)

    # endregion

    # region    Layer adding functions

    def add_outer_and_art_bevels_on_side(self, side):
        light_mask = psd.getLayer(self.textbox_size + " Light", self.bevels_mask_groups[side])
        dark_mask = psd.getLayer(self.textbox_size + " Dark", self.bevels_mask_groups[side])

        for (mask, layer) in [
            (light_mask, self.bevels_light_groups[side]),
            (dark_mask, self.bevels_dark_groups[side])
        ]:
            psd.copy_vector_mask(mask, layer)
            enable(self.identity_advanced[side], layer)

    def add_textbox_bevels_on_side(self, side, identity=None):
        if self.has_textbox_bevels[side]:
            if identity is None: identity = self.identity_advanced[side]
            tr, bl, textbox_bevel = self.copy_textbox_bevel_masks_on_side(identity, side)

            if (identity == "U" or identity == "R") and not self.is_split_fade[side]:
                enable(self.textbox_size, textbox_bevel)

    def copy_textbox_bevel_masks_on_side(self, identity, side) -> tuple[LayerSet, LayerSet, LayerSet]:
        sized_bevel_masks = psd.getLayerSet(self.textbox_size, self.textbox_bevels_mask_groups[side])
        textbox_bevel = psd.getLayerSet(identity, self.textbox_bevels_groups[side])
        enable(textbox_bevel)

        top_right = psd.getLayerSet("TR", textbox_bevel)
        bottom_left = psd.getLayerSet("BL", textbox_bevel)
        top_right_mask = psd.getLayer(self.textbox_bevel_thickness[side] + " TR", sized_bevel_masks)
        bottom_left_mask = psd.getLayer(self.textbox_bevel_thickness[side] + " BL", sized_bevel_masks)

        psd.copy_vector_mask(top_right_mask, top_right)
        psd.copy_vector_mask(bottom_left_mask, bottom_left)

        return top_right, bottom_left, textbox_bevel

    def dual_fade_frame_texture_on_side(self, side):
        (top_mask_name, _, top_layer, bottom_layer) = self.dual_fade_order[side]

        top_mask = psd.getLayer(top_mask_name, self.mask_groups[side])
        top_frame_layer = psd.getLayer(top_layer, self.frame_texture_groups[side])
        bottom_frame_layer = psd.getLayer(bottom_layer, self.frame_texture_groups[side])

        psd.copy_layer_mask(top_mask, top_frame_layer)

        enable(top_frame_layer)
        enable(bottom_frame_layer)

    def dual_fade_nonland_textbox_on_side(self, side, colors_override = None):
        color_source = self.dual_fade_order[side] if colors_override is None else colors_override
        (top_mask_name, _, top_layer, bottom_layer) = color_source

        top_mask = psd.getLayer(top_mask_name, self.mask_groups[side])
        top_textbox_layer = psd.getLayer(top_layer, self.textbox_groups[side])
        bottom_textbox_layer = psd.getLayer(bottom_layer, self.textbox_groups[side])

        psd.copy_layer_mask(top_mask, top_textbox_layer)

        enable(top_textbox_layer)
        enable(bottom_textbox_layer)

    def dual_fade_textbox_bevels_on_side(self, side):
        if not self.has_textbox_bevels[side]: return

        (top_mask_name, bottom_mask_name, top_layer, bottom_layer) = self.dual_fade_order[side]

        top_mask = psd.getLayer(top_mask_name, self.mask_groups[side])
        bottom_mask = psd.getLayer(bottom_mask_name, self.mask_groups[side])

        for mask_layer, layer in [
            (top_mask, top_layer),
            (bottom_mask, bottom_layer),
        ]:
            self.add_textbox_bevels(identity=layer)
            psd.copy_layer_mask(mask_layer, psd.getLayerSet(layer, self.textbox_bevels_groups[side]))

    def dual_fade_bevels_on_side(self, side):

        (top_mask_name, bottom_mask_name, top_layer, bottom_layer) = self.dual_fade_order[side]

        top_mask = psd.getLayer(top_mask_name, self.mask_groups[side])
        bottom_mask = psd.getLayer(bottom_mask_name, self.mask_groups[side])
        light_mask = psd.getLayer(self.textbox_size + " Light", self.bevels_mask_groups[side])
        dark_mask = psd.getLayer(self.textbox_size + " Dark", self.bevels_mask_groups[side])

        light_group = self.bevels_light_groups[side]
        dark_group = self.bevels_dark_groups[side]

        psd.copy_vector_mask(light_mask, light_group)
        psd.copy_vector_mask(dark_mask, dark_group)

        for (mask, layer, group) in [
            (top_mask, top_layer, light_group),
            (top_mask, top_layer, dark_group),
            (bottom_mask, bottom_layer, light_group),
            (bottom_mask, bottom_layer, dark_group),
        ]:
            enable(layer, group)
            psd.copy_layer_mask(mask, psd.getLayer(layer, group))

    def position_type_line(self):
        """Positions the type line elements vertically based on the textbox size"""
        match self.textbox_size:
            case "Room":
                offset = 0 #Unknown
            case _:
                offset = 0

        for symbol in self.expansion_symbols:
            if symbol: symbol.translate(0, offset)

        for i in range(2):
            self.text_layer_type[i].translate(0, offset)

    def add_tombstone(self):
        enable("Tombstone", self.text_groups[1])

    def add_nonland_frame_texture(self):
        for i in range(2):
            if self.is_split_fade[i]:
                self.dual_fade_frame_texture_on_side(i)
                self.dual_fade_bevels_on_side(i)
            else:
                enable(self.frame_textures[i])
                self.add_outer_and_art_bevels_on_side(i)

    def add_nonland_textbox(self):
        for i in range(2):
            if self.is_split_fade[i]:
                self.dual_fade_nonland_textbox_on_side(i)
                if self.cfg_dual_textbox_bevels:
                    self.dual_fade_textbox_bevels_on_side(i)
                else:
                    self.add_textbox_bevels_on_side(i)
            else:
                enable(self.textbox_textures[i])
                self.add_textbox_bevels_on_side(i)

    def apply_textbox_shape(self):
        for i in range(2):
            # Enables rasterized textbox for black textboxes
            if self.has_irregular_textbox and self.identity_advanced[i] == "B":
                enable(f"B {self.textbox_size}", self.textbox_groups[i])
            else:
                # Enables vector mask for vectorized textboxes (including green)
                enable(self.textbox_shapes[i])

    def add_outlines(self):
        for i in range(2):
            enable(self.art_outlines[i])
            if self.textbox_outlines[i]: enable(self.textbox_outlines[i])

    def add_textbox_decorations(self):
        """Adds fx to textboxes when appropriate"""
        for i in range(2):
            # Applies dropshadow effect to green textbox
            if self.identity_advanced[i] == "G":
                psd.copy_layer_fx(psd.getLayer("G", self.textbox_effects_groups[i]), self.textbox_groups[i])

    def add_textbox(self):
        self.add_nonland_textbox()
        self.apply_textbox_shape()
        self.add_textbox_decorations()

    def enable_frame_layers(self):
        for i in range(2):
            enable(self.frame_masks[i])
            if self.is_promo_star: enable("Promo Star", self.text_groups[i])

        self.add_outlines()
        self.add_nonland_frame_texture()
        self.add_textbox()
        self.position_type_line()
        self.adjust_mana_cost()

        if self.is_aftermath: self.add_tombstone()

    # endregion