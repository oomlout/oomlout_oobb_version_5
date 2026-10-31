include <../gridfinity_tray_raw/ostat/gridfinity_extended_openscad/modules/functions_environment.scad>
use <../gridfinity_tray_raw/ostat/gridfinity_extended_openscad/modules/module_gridfinity_cup.scad>

function _gridfinity_dimension(value) = is_num(value) ? [value, 0] : value;

// Reuse the standard pad profile; only the pad sizes and placement differ.
use <../gridfinity_tray_raw/ostat/gridfinity_extended_openscad/modules/module_gridfinity.scad>;
use <../gridfinity_tray_raw/ostat/gridfinity_extended_openscad/modules/module_gridfinity_efficient_floor.scad>;

function _quarter_valid(units) =
    units > 0 && abs(units * 4 - round(units * 4)) < 0.0000001;

function _quarter_remainder(units) = round(units * 4) % 2 == 1;

// Entries are [start, length] in grid units. No quarter-by-quarter pads.
function _quarter_segments(units, alignment = "near") =
    let(whole = floor(units), remainder = round((units - whole) * 4),
        segments = concat(
            [for (i = [0:1:whole - 1]) [i, 1]],
            remainder >= 2 ? [[whole, 0.5]] : [],
            remainder % 2 == 1 ? [[whole + (remainder >= 2 ? 0.5 : 0), 0.25]] : []))
    alignment == "far"
        ? [for (segment = segments) [units - segment[0] - segment[1], segment[1]]]
        : segments;

module _quarter_bottom(width, height, align_x, align_y) {
    intersection() {
        children();
        union() {
            for (x = _quarter_segments(width, align_x),
                 y = _quarter_segments(height, align_y))
                translate([x[0] * env_pitch().x, y[0] * env_pitch().y, 0])
                    pad_oversize(num_x = x[1], num_y = y[1]);
            // Standard feet merge into the continuous floor at z=5 mm.
            // The oversize pad tops overlap this mask, so no seams are introduced.
            translate([-env_pitch().x, -env_pitch().y, 5])
                cube([(width + 2) * env_pitch().x,
                      (height + 2) * env_pitch().y,
                      max(0, env_numz()) * env_pitch().z + 100]);
        }
    }
}

// Limit the upstream efficient cavity to recesses that follow our mixed feet.
// children(0) is the flat-floor tray; children(1) is the upstream efficient tray.
// Keeping only their difference preserves wall, divider and attachment geometry.
module _quarter_efficient_floor(width, height, align_x, align_y,
    floor_style, floor_thickness, wall_thickness, grid_height) {
    difference() {
        children(0);
        difference() {
            union() {
                for (x = _quarter_segments(width, align_x),
                     y = _quarter_segments(height, align_y))
                    translate([x[0] * env_pitch().x, y[0] * env_pitch().y, 0])
                        // A 0.01 mm inset avoids coincident cavity faces in the
                        // boolean operations and slightly increases floor thickness.
                        translate([x[1] * env_pitch().x / 2, y[1] * env_pitch().y / 2, 0.01])
                        scale([1 - 0.02 / (x[1] * env_pitch().x),
                               1 - 0.02 / (y[1] * env_pitch().y), 1])
                        translate([-x[1] * env_pitch().x / 2, -y[1] * env_pitch().y / 2, 0])
                        EfficientFloor(
                            num_x = x[1], num_y = y[1],
                            floor_thickness = floor_thickness,
                            margins = 2.6 - wallThickness(wall_thickness, env_numz()),
                            floorRounded = floor_style == "rounded",
                            floorSmooth = floor_style == "smooth" ? 1 : 0,
                            efficientFloorGridHeight = grid_height);
            }
            children(1);
        }
    }
}

module gridfinity_tray_quarter_increment(
    gridfinity_width = 2,
    gridfinity_depth = 3,
    gridfinity_height = 1,
    filled_in = "disabled",
    wall_thickness = 0,
    headroom = 0.8,
    lip_style = "normal",
    lip_side_relief_trigger = [1, 1],
    lip_top_relief_height = -1,
    lip_top_relief_width = -1,
    lip_top_notches = true,
    lip_clip_position = "disabled",
    lip_non_blocking = false,
    height_includes_lip = false,
    chamber_wall_thickness = [1.2, 1.2],
    chamber_wall_headroom = 0,
    chamber_wall_top_radius = 0,
    vertical_chambers = 1,
    vertical_separator_bend_separation = 0,
    vertical_separator_bend_angle = 45,
    vertical_separator_bend_position = 0,
    vertical_separator_cut_depth = 0,
    horizontal_chambers = 1,
    horizontal_separator_bend_separation = 0,
    horizontal_separator_bend_angle = 45,
    horizontal_separator_bend_position = 0,
    horizontal_separator_cut_depth = 0,
    vertical_irregular_subdivisions = false,
    vertical_separator_config = "10.5|21|42|50|60",
    horizontal_irregular_subdivisions = false,
    horizontal_separator_config = "10.5|21|42|50|60",
    enable_magnets = false,
    enable_screws = false,
    magnet_size = [6.5, 2.4],
    magnet_easy_release = "auto",
    magnet_side_access = "disabled",
    magnet_captive_height = 0,
    magnet_crush_depth = 0,
    magnet_chamfer = 0,
    screw_size = [3, 6],
    center_magnet_size = [0, 0],
    hole_overhang_remedy = 2,
    box_corner_attachments_only = "enabled",
    floor_thickness = 0.7,
    cavity_floor_radius = -1,
    efficient_floor = "on",
    sub_pitch = 1,
    flat_base = "off",
    spacer = false,
    minimum_printable_pad_size = 0.2,
    flat_base_rounded_radius = -1,
    flat_base_rounded_easyPrint = -1,
    align_grid_x = "near",
    align_grid_y = "near",
    label_style = "disabled",
    label_position = "left",
    label_dividers = "disabled",
    label_size = [0, 14, 0, 0.6],
    label_relief = [0, 0, 0, 0.6],
    label_walls = [0, 1, 0, 0],
    sliding_lid_enabled = false,
    sliding_lid_thickness = 0,
    sliding_lid_min_wall_thickness = 0,
    sliding_lid_min_support = 0,
    sliding_lid_clearance = 0.1,
    sliding_lid_pull_style = "disabled",
    sliding_lid_nub_size = 0.5,
    fingerslide = "none",
    fingerslide_radius = -3,
    fingerslide_walls = [1, 0, 0, 0],
    fingerslide_lip_aligned = true,
    tapered_corner = "none",
    tapered_corner_size = 10,
    tapered_setback = -1,
    wallpattern_enabled = false,
    wallpattern_style = "hexgrid",
    wallpattern_strength = 2,
    wallpattern_walls = [1, 1, 1, 1],
    wallpattern_rotate_grid = false,
    wallpattern_cell_size = [10, 10],
    wallpattern_dividers_enabled = "disabled",
    wallpattern_hole_sides = 6,
    wallpattern_hole_radius = 0.5,
    wallpattern_fill = "none",
    wallpattern_border = 0,
    wallpattern_depth = 0,
    wallpattern_pattern_grid_chamfer = 0,
    wallpattern_pattern_voronoi_noise = 0.75,
    wallpattern_pattern_brick_weight = 5,
    wallpattern_pattern_quality = 0.4,
    wallpattern_colored = "disabled",
    floorpattern_enabled = false,
    floorpattern_style = "hexgrid",
    floorpattern_strength = 2,
    floorpattern_rotate_grid = false,
    floorpattern_cell_size = [10, 10],
    floorpattern_hole_sides = 6,
    floorpattern_hole_radius = 0.5,
    floorpattern_fill = "crop",
    floorpattern_border = 0,
    floorpattern_depth = 0,
    floorpattern_pattern_grid_chamfer = 0,
    floorpattern_pattern_voronoi_noise = 0.75,
    floorpattern_pattern_brick_weight = 5,
    floorpattern_pattern_quality = 0.4,
    wallcutout_vertical = "disabled",
    wallcutout_vertical_position = [-2, -0.5, -0.5, -0.5],
    wallcutout_vertical_width = 0,
    wallcutout_vertical_angle = 70,
    wallcutout_vertical_height = 0,
    wallcutout_vertical_corner_radius = 5,
    wallcutout_horizontal = "disabled",
    wallcutout_horizontal_position = [-2, -0.5, -0.5, -0.5],
    wallcutout_horizontal_width = 0,
    wallcutout_horizontal_angle = 70,
    wallcutout_horizontal_height = 0,
    wallcutout_horizontal_corner_radius = 5,
    extension_x_enabled = "disabled",
    extension_x_position = 0.5,
    extension_y_enabled = "disabled",
    extension_y_position = 0.5,
    extension_tabs_enabled = true,
    extension_tab_size = [10, 0, 0, 0],
    text_1 = false,
    text_size = 0,
    text_depth = 0.3,
    text_offset = [0, 0],
    text_font = "Aldo",
    text_2 = false,
    text_2_text = "Gridfinity Extended",
    cut = [0, 0, 0],
    enable_help = "disabled",
    pitch = [gf_pitch, gf_pitch, gf_zpitch],
    clearance = [0.5, 0.5, 0],
    set_colour = "enable",
    render_position = "center",
    fa = 6,
    fs = 0.4,
    fn = 0,
    random_seed = 0,
    force_render = true
) {
    width = _gridfinity_dimension(gridfinity_width);
    depth = _gridfinity_dimension(gridfinity_height);
    height = _gridfinity_dimension(gridfinity_depth);
    units_x = calcDimension(gridfinity_width, "width", pitch[0]);
    units_y = calcDimension(gridfinity_height, "height", pitch[1]);
    assert(_quarter_valid(units_x) && _quarter_valid(units_y),
        "Quarter-increment dimensions must be positive multiples of 0.25.");
    assert(!(_quarter_remainder(units_x) && _quarter_remainder(units_y)),
        "Quarter increments are supported on only one axis per tray.");
    assert((align_grid_x == "near" || align_grid_x == "far")
        && (align_grid_y == "near" || align_grid_y == "far"),
        "Quarter-increment feet require near or far grid alignment.");

    $fa = fa;
    $fs = fs;
    $fn = fn;

    module tray_with_floor(floor_style) {
        gridfinity_cup(
            width = width,
            depth = depth,
            height = height,
            filled_in = filled_in,
            label_settings = LabelSettings(
                labelStyle = label_style,
                labelPosition = label_position,
                labelSize = label_size,
                labelRelief = label_relief,
                labelWalls = label_walls,
                labelDividers = label_dividers
            ),
            finger_slide_settings = FingerSlideSettings(
                type = fingerslide,
                radius = fingerslide_radius,
                walls = fingerslide_walls,
                lip_aligned = fingerslide_lip_aligned
            ),
            cupBase_settings = CupBaseSettings(
                magnetSize = enable_magnets ? magnet_size : [0, 0],
                magnetEasyRelease = magnet_easy_release,
                magnetSideAccess = magnet_side_access,
                magnetCaptiveHeight = magnet_captive_height,
                magnetCrushDepth = magnet_crush_depth,
                magnetChamfer = magnet_chamfer,
                centerMagnetSize = center_magnet_size,
                screwSize = enable_screws ? screw_size : [0, 0],
                holeOverhangRemedy = hole_overhang_remedy,
                cornerAttachmentsOnly = box_corner_attachments_only,
                floorThickness = floor_thickness,
                cavityFloorRadius = cavity_floor_radius,
                efficientFloor = floor_style,
                subPitch = 1,
                // Keep the standard floor height and carve the fractional feet below it.
                flatBase = "off",
                spacer = spacer,
                minimumPrintablePadSize = minimum_printable_pad_size,
                flatBaseRoundedRadius = flat_base_rounded_radius,
                flatBaseRoundedEasyPrint = flat_base_rounded_easyPrint,
                alignGrid = [align_grid_x, align_grid_y]
            ),
            wall_thickness = wall_thickness,
            vertical_chambers = ChamberSettings(
                chambers_count = vertical_chambers,
                chamber_wall_thickness = chamber_wall_thickness,
                chamber_wall_headroom = chamber_wall_headroom,
                chamber_wall_top_radius = chamber_wall_top_radius,
                separator_bend_position = vertical_separator_bend_position,
                separator_bend_angle = vertical_separator_bend_angle,
                separator_bend_separation = vertical_separator_bend_separation,
                separator_cut_depth = vertical_separator_cut_depth,
                irregular_subdivisions = vertical_irregular_subdivisions,
                separator_config = vertical_separator_config
            ),
            horizontal_chambers = ChamberSettings(
                chambers_count = horizontal_chambers,
                chamber_wall_thickness = chamber_wall_thickness,
                chamber_wall_headroom = chamber_wall_headroom,
                chamber_wall_top_radius = chamber_wall_top_radius,
                separator_bend_position = horizontal_separator_bend_position,
                separator_bend_angle = horizontal_separator_bend_angle,
                separator_bend_separation = horizontal_separator_bend_separation,
                separator_cut_depth = horizontal_separator_cut_depth,
                irregular_subdivisions = horizontal_irregular_subdivisions,
                separator_config = horizontal_separator_config
            ),
            lip_settings = LipSettings(
                lipStyle = lip_style,
                lipSideReliefTrigger = lip_side_relief_trigger,
                lipTopReliefHeight = lip_top_relief_height,
                lipTopReliefWidth = lip_top_relief_width,
                lipNotch = lip_top_notches,
                lipClipPosition = lip_clip_position,
                lipNonBlocking = lip_non_blocking
            ),
            headroom = headroom,
            tapered_corner = tapered_corner,
            tapered_corner_size = tapered_corner_size,
            tapered_setback = tapered_setback,
            wallpattern_walls = wallpattern_walls,
            wallpattern_dividers_enabled = wallpattern_dividers_enabled,
            wall_pattern_settings = PatternSettings(
                patternEnabled = wallpattern_enabled,
                patternStyle = wallpattern_style,
                patternRotate = wallpattern_rotate_grid,
                patternFill = wallpattern_fill,
                patternBorder = wallpattern_border,
                patternDepth = wallpattern_depth,
                patternCellSize = wallpattern_cell_size,
                patternHoleSides = wallpattern_hole_sides,
                patternStrength = wallpattern_strength,
                patternHoleRadius = wallpattern_hole_radius,
                patternGridChamfer = wallpattern_pattern_grid_chamfer,
                patternVoronoiNoise = wallpattern_pattern_voronoi_noise,
                patternBrickWeight = wallpattern_pattern_brick_weight,
                patternFs = wallpattern_pattern_quality,
                patternColored = wallpattern_colored
            ),
            floor_pattern_settings = PatternSettings(
                patternEnabled = floorpattern_enabled,
                patternStyle = floorpattern_style,
                patternRotate = floorpattern_rotate_grid,
                patternFill = floorpattern_fill,
                patternBorder = floorpattern_border,
                patternDepth = floorpattern_depth,
                patternCellSize = floorpattern_cell_size,
                patternHoleSides = floorpattern_hole_sides,
                patternStrength = floorpattern_strength,
                patternHoleRadius = floorpattern_hole_radius,
                patternGridChamfer = floorpattern_pattern_grid_chamfer,
                patternVoronoiNoise = floorpattern_pattern_voronoi_noise,
                patternBrickWeight = floorpattern_pattern_brick_weight,
                patternFs = floorpattern_pattern_quality
            ),
            wallcutout_vertical_settings = WallCutoutSettings(
                type = wallcutout_vertical,
                position = wallcutout_vertical_position,
                width = wallcutout_vertical_width,
                angle = wallcutout_vertical_angle,
                height = wallcutout_vertical_height,
                corner_radius = wallcutout_vertical_corner_radius
            ),
            wallcutout_horizontal_settings = WallCutoutSettings(
                type = wallcutout_horizontal,
                position = wallcutout_horizontal_position,
                width = wallcutout_horizontal_width,
                angle = wallcutout_horizontal_angle,
                height = wallcutout_horizontal_height,
                corner_radius = wallcutout_horizontal_corner_radius
            ),
            extendable_Settings = ExtendableSettings(
                extendablexEnabled = extension_x_enabled,
                extendablexPosition = extension_x_position,
                extendableyEnabled = extension_y_enabled,
                extendableyPosition = extension_y_position,
                extendableTabsEnabled = extension_tabs_enabled,
                extendableTabSize = extension_tab_size
            ),
            sliding_lid_settings = SlidingLidSettings(
                enabled = sliding_lid_enabled,
                thickness = sliding_lid_thickness,
                min_wall_thickness = sliding_lid_min_wall_thickness,
                min_support = sliding_lid_min_support,
                clearance = sliding_lid_clearance,
                pull_style = sliding_lid_pull_style,
                nub_size = sliding_lid_nub_size
            ),
            cupBaseTextSettings = CupBaseTextSettings(
                baseTextLine1Enabled = text_1,
                baseTextLine2Enabled = text_2,
                baseTextLine2Value = text_2_text,
                baseTextFontSize = text_size,
                baseTextFont = text_font,
                baseTextDepth = text_depth,
                baseTextOffset = text_offset
            )
        );
    }

    floor_style = validateEfficientFloor(efficient_floor);
    set_environment(
        width = width, depth = depth, height = height,
        height_includes_lip = height_includes_lip,
        lip_enabled = lip_style != "none", render_position = render_position,
        help = enable_help, pitch = pitch, clearance = clearance, cut = cut,
        setColour = set_colour, randomSeed = random_seed, force_render = force_render
    )
    _quarter_bottom(units_x, units_y, align_grid_x, align_grid_y)
    if (floor_style == "off") {
        tray_with_floor("off");
    } else {
        _quarter_efficient_floor(
            units_x, units_y, align_grid_x, align_grid_y, floor_style,
            floor_thickness, wall_thickness,
            max(5, enable_magnets ? magnet_size[1] : 0,
                   enable_screws ? screw_size[1] : 0) + floor_thickness
        ) {
            tray_with_floor("off");
            tray_with_floor(floor_style);
        }
    }
}
