/* Beckeringh Palace Figma adapter. The compiler replaces the marker below. */
const BP_MANIFEST = __BECKERINGH_FIGMA_MANIFEST__;

const COLLECTION_NAMES = Object.freeze({
  primitives: "Color Primitives",
  palette: "Palette",
  material: "Material",
  spacing: "Spacing",
  radius: "Radius",
  border: "Border",
  motion: "Motion",
  typography: "Typography",
});

function assertManifest(manifest) {
  if (!manifest || manifest.schema_version !== 2) {
    throw new Error("Beckeringh Palace Figma adapter requires schema_version 2");
  }
  if (!manifest.product || !/^sha256:[0-9a-f]+$/.test(manifest.product.snapshot || "")) {
    throw new Error("Figma manifest requires a sha256 snapshot identity");
  }
  for (const key of ["theme", "assets", "appearances", "components", "variants", "compositions", "layouts"]) {
    if (!(key in manifest)) throw new Error(`Figma manifest misses '${key}'`);
  }
  return manifest;
}

function px(value) {
  if (value === "0") return 0;
  const match = /^(-?(?:0|[1-9][0-9]*)(?:\.[0-9]+)?)px$/.exec(value);
  if (!match) throw new Error(`Expected px value, got '${value}'`);
  return Number(match[1]);
}

function ms(value) {
  const match = /^(0|[1-9][0-9]*(?:\.[0-9]+)?)ms$/.exec(value);
  if (!match) throw new Error(`Expected ms value, got '${value}'`);
  return Number(match[1]);
}

function hexColor(value) {
  const match = /^#([0-9a-fA-F]{6})([0-9a-fA-F]{2})?$/.exec(value);
  if (!match) throw new Error(`Expected hex color, got '${value}'`);
  const rgb = match[1];
  return {
    r: parseInt(rgb.slice(0, 2), 16) / 255,
    g: parseInt(rgb.slice(2, 4), 16) / 255,
    b: parseInt(rgb.slice(4, 6), 16) / 255,
    a: match[2] ? parseInt(match[2], 16) / 255 : 1,
  };
}

function cssCodeSyntax(name) {
  return `var(${name})`;
}

function paletteScopes(role) {
  if (role === "foreground") return ["TEXT_FILL", "SHAPE_FILL"];
  if (role === "background" || role === "surface") return ["FRAME_FILL", "SHAPE_FILL"];
  return ["FRAME_FILL", "SHAPE_FILL", "STROKE_COLOR"];
}

function materialScopes(role) {
  if (role.includes("foreground") || role === "muted" || role === "disabled") {
    return ["TEXT_FILL", "SHAPE_FILL"];
  }
  if (role === "outline") return ["STROKE_COLOR"];
  if (role === "canvas" || role === "surface" || role === "raised" || role === "field" || role === "transparent" || role.endsWith("-surface")) {
    return ["FRAME_FILL", "SHAPE_FILL"];
  }
  return ["FRAME_FILL", "SHAPE_FILL", "STROKE_COLOR"];
}

function splitCssShadows(value) {
  const parts = [];
  let depth = 0;
  let start = 0;
  for (let index = 0; index < value.length; index += 1) {
    const char = value[index];
    if (char === "(") depth += 1;
    if (char === ")") depth -= 1;
    if (char === "," && depth === 0) {
      parts.push(value.slice(start, index).trim());
      start = index + 1;
    }
  }
  parts.push(value.slice(start).trim());
  return parts.filter(Boolean);
}

/** @returns {DropShadowEffect[]} */
function parseCssShadow(value) {
  if (value === "none") return [];
  return splitCssShadows(value).map((part) => {
    const length = "(-?(?:\\d+(?:\\.\\d+)?)(?:px)?)";
    const pattern = new RegExp(
      `^${length}\\s+${length}\\s+${length}(?:\\s+${length})?\\s+` +
      "rgba\\(\\s*(\\d+)\\s*,\\s*(\\d+)\\s*,\\s*(\\d+)\\s*,\\s*(0|1|0?\\.\\d+)\\s*\\)$",
    );
    const match = pattern.exec(part);
    if (!match) throw new Error(`Unsupported shadow '${part}'`);
    const numericLength = (token) => Number(token.replace("px", ""));
    /** @type {DropShadowEffect} */
    const effect = {
      type: "DROP_SHADOW",
      color: {
        r: Number(match[5]) / 255,
        g: Number(match[6]) / 255,
        b: Number(match[7]) / 255,
        a: Number(match[8]),
      },
      offset: {x: numericLength(match[1]), y: numericLength(match[2])},
      radius: numericLength(match[3]),
      spread: match[4] === undefined ? 0 : numericLength(match[4]),
      visible: true,
      blendMode: "NORMAL",
    };
    return effect;
  });
}

function textMetrics(role) {
  const size = px(role.font_size);
  /** @type {LineHeight} */
  const lineHeight = role.line_height === "normal"
    ? {unit: "AUTO"}
    : {unit: "PERCENT", value: Number(role.line_height) * 100};
  /** @type {LetterSpacing} */
  const letterSpacing = role.letter_spacing === "normal"
    ? {unit: "PERCENT", value: 0}
    : {unit: "PERCENT", value: Number(role.letter_spacing.replace("em", "")) * 100};
  return {size, lineHeight, letterSpacing};
}

function desiredState(manifest) {
  assertManifest(manifest);
  const theme = manifest.theme;
  const components = manifest.components.map((component) => {
    const profiles = manifest.variants.filter((variant) => variant.component === component.id);
    const needsBase = manifest.compositions.some((composition) => composition.instances.some(
      (instance) => instance.component === component.id && instance.variant === null,
    ));
    const variants = [];
    if (needsBase) variants.push({profile: "base", state: "rest", appearance: component.appearance});
    for (const profile of profiles) {
      for (const [state, appearance] of Object.entries(profile.states)) {
        variants.push({profile: profile.id, state, appearance});
      }
    }
    return {...component, figmaVariants: variants};
  });
  return {
    schemaVersion: manifest.schema_version,
    snapshot: manifest.product.snapshot,
    collections: {
      primitives: Object.keys(theme.color_primitives).length,
      palette: Object.keys(theme.palet.rollen).length,
      material: Object.keys(theme.materiaal.rollen).length,
      spacing: Object.keys(theme.spacing.rollen).length,
      radius: Object.keys(theme.radius.rollen).length,
      border: Object.keys(theme.border.rollen).length,
      motion: Object.keys(theme.motion.rollen).length,
      typography: Object.keys(theme.typeschaal.rollen).length * 5,
    },
    textStyles: Object.keys(theme.typeschaal.rollen),
    effectStyles: Object.keys(theme.shadow.rollen),
    assets: manifest.assets.map((asset) => asset.id),
    components,
    compositions: manifest.compositions.map((composition) => composition.id),
    layouts: manifest.layouts.map((layout) => layout.id),
  };
}

/** @param {PluginAPI} figmaApi */
async function ensureCollection(figmaApi, name) {
  const collections = await figmaApi.variables.getLocalVariableCollectionsAsync();
  let collection = collections.find((candidate) => candidate.name === name);
  if (!collection) collection = figmaApi.variables.createVariableCollection(name);
  if (collection.modes.length !== 1) {
    throw new Error(`Collection '${name}' must have exactly one mode`);
  }
  if (collection.modes[0].name !== "Value") {
    collection.renameMode(collection.modes[0].modeId, "Value");
  }
  return collection;
}

/** @param {PluginAPI} figmaApi */
async function variableIndex(figmaApi) {
  const variables = await figmaApi.variables.getLocalVariablesAsync();
  const result = new Map();
  for (const variable of variables) {
    result.set(`${variable.variableCollectionId}\u0000${variable.name}`, variable);
  }
  return result;
}

function variableKey(collection, name) {
  return `${collection.id}\u0000${name}`;
}

/** @param {PluginAPI} figmaApi */
function ensureVariable(figmaApi, index, collection, name, type, value, scopes, codeSyntax) {
  const key = variableKey(collection, name);
  let variable = index.get(key);
  if (variable && variable.resolvedType !== type) {
    throw new Error(`Variable '${name}' has type '${variable.resolvedType}', expected '${type}'`);
  }
  if (!variable) {
    variable = figmaApi.variables.createVariable(name, collection, type);
    index.set(key, variable);
  }
  variable.scopes = scopes;
  if (codeSyntax) variable.setVariableCodeSyntax("WEB", codeSyntax);
  variable.setValueForMode(collection.modes[0].modeId, value);
  return variable;
}

/** @param {PluginAPI} figmaApi */
function ensureAlias(figmaApi, index, collection, name, target, scopes, codeSyntax) {
  return ensureVariable(
    figmaApi,
    index,
    collection,
    name,
    "COLOR",
    figmaApi.variables.createVariableAlias(target),
    scopes,
    codeSyntax,
  );
}

/** @param {PluginAPI} figmaApi */
async function syncFoundations(figmaApi, manifest) {
  const theme = manifest.theme;
  const collections = {};
  for (const [key, name] of Object.entries(COLLECTION_NAMES)) {
    collections[key] = await ensureCollection(figmaApi, name);
  }
  const index = await variableIndex(figmaApi);
  const refs = {primitives: {}, palette: {}, material: {}, spacing: {}, radius: {}, border: {}, motion: {}, typography: {}};

  for (const [id, value] of Object.entries(theme.color_primitives)) {
    refs.primitives[id] = ensureVariable(
      figmaApi, index, collections.primitives, id, "COLOR", hexColor(value), [],
      cssCodeSyntax(`--bp-color-${id}`),
    );
  }
  for (const [role, color] of Object.entries(theme.palet.rollen)) {
    const primitive = refs.primitives[color.color_id];
    if (!primitive) throw new Error(`Palette '${role}' references missing color '${color.color_id}'`);
    refs.palette[role] = ensureAlias(
      figmaApi, index, collections.palette, role, primitive, paletteScopes(role),
      cssCodeSyntax(`--bp-theme-${role}`),
    );
  }
  for (const [role, color] of Object.entries(theme.materiaal.rollen)) {
    const primitive = refs.primitives[color.color_id];
    if (!primitive) throw new Error(`Material '${role}' references missing color '${color.color_id}'`);
    refs.material[role] = ensureAlias(
      figmaApi, index, collections.material, role, primitive, materialScopes(role),
      cssCodeSyntax(`--bp-material-${role}`),
    );
  }
  for (const [role, value] of Object.entries(theme.spacing.rollen)) {
    refs.spacing[role] = ensureVariable(
      figmaApi, index, collections.spacing, role, "FLOAT", px(value), ["GAP"],
      cssCodeSyntax(`--bp-spacing-${role}`),
    );
  }
  for (const [role, value] of Object.entries(theme.radius.rollen)) {
    refs.radius[role] = ensureVariable(
      figmaApi, index, collections.radius, role, "FLOAT", px(value), ["CORNER_RADIUS"],
      cssCodeSyntax(`--bp-radius-${role}`),
    );
  }
  for (const [role, value] of Object.entries(theme.border.rollen)) {
    const numeric = role !== "style";
    refs.border[role] = ensureVariable(
      figmaApi, index, collections.border, role, numeric ? "FLOAT" : "STRING",
      numeric ? px(value) : value, numeric ? ["STROKE_FLOAT"] : [],
      cssCodeSyntax(`--bp-border-${role}`),
    );
  }
  for (const [role, value] of Object.entries(theme.motion.rollen)) {
    let normalized = value;
    if (/ms$/.test(value)) normalized = `${ms(value)}ms`;
    refs.motion[role] = ensureVariable(
      figmaApi, index, collections.motion, role, "STRING", normalized, [],
      cssCodeSyntax(`--bp-motion-${role.replace("_", "-")}`),
    );
  }

  for (const [role, definition] of Object.entries(theme.typeschaal.rollen)) {
    const metrics = textMetrics(definition);
    const base = `type/${role}`;
    refs.typography[`${role}/font-family`] = ensureVariable(
      figmaApi, index, collections.typography, `${base}/font-family`, "STRING",
      definition.font_family[0], ["FONT_FAMILY"], cssCodeSyntax(`--bp-type-${role}-font`),
    );
    refs.typography[`${role}/font-size`] = ensureVariable(
      figmaApi, index, collections.typography, `${base}/font-size`, "FLOAT",
      metrics.size, ["FONT_SIZE"], cssCodeSyntax(`--bp-type-${role}`),
    );
    refs.typography[`${role}/font-weight`] = ensureVariable(
      figmaApi, index, collections.typography, `${base}/font-weight`, "FLOAT",
      Number(definition.font_weight), ["FONT_WEIGHT"], cssCodeSyntax(`--bp-type-${role}-weight`),
    );
    const lineHeightValue = definition.line_height === "normal"
      ? 0
      : metrics.size * Number(definition.line_height);
    refs.typography[`${role}/line-height`] = ensureVariable(
      figmaApi, index, collections.typography, `${base}/line-height`, "FLOAT",
      lineHeightValue, ["LINE_HEIGHT"], cssCodeSyntax(`--bp-type-${role}-line-height`),
    );
    const trackingValue = definition.letter_spacing === "normal"
      ? 0
      : metrics.size * Number(definition.letter_spacing.replace("em", ""));
    refs.typography[`${role}/letter-spacing`] = ensureVariable(
      figmaApi, index, collections.typography, `${base}/letter-spacing`, "FLOAT",
      trackingValue, ["LETTER_SPACING"], cssCodeSyntax(`--bp-type-${role}-letter-spacing`),
    );
  }
  return {collections, refs};
}

/** @param {PluginAPI} figmaApi */
async function availableFontName(figmaApi, definition) {
  const allFonts = await figmaApi.listAvailableFontsAsync();
  const family = definition.font_family[0];
  const preferred = {
    "400": ["Regular", "Normal"],
    "500": ["Medium"],
    "600": ["SemiBold", "Semi Bold", "DemiBold", "Demi Bold"],
    "700": ["Bold"],
  }[definition.font_weight] || [];
  for (const style of preferred) {
    if (allFonts.some((entry) => entry.fontName.family === family && entry.fontName.style === style)) {
      return {family, style};
    }
  }
  throw new Error(`Font style for '${family}' weight ${definition.font_weight} is unavailable`);
}

/** @param {PluginAPI} figmaApi */
async function syncTextStyles(figmaApi, manifest) {
  const styles = await figmaApi.getLocalTextStylesAsync();
  const result = {};
  for (const [role, definition] of Object.entries(manifest.theme.typeschaal.rollen)) {
    const name = `Type/${role}`;
    let style = styles.find((candidate) => candidate.name === name);
    if (!style) {
      style = figmaApi.createTextStyle();
      style.name = name;
      styles.push(style);
    }
    const fontName = await availableFontName(figmaApi, definition);
    await figmaApi.loadFontAsync(fontName);
    const metrics = textMetrics(definition);
    style.fontName = fontName;
    style.fontSize = metrics.size;
    style.lineHeight = metrics.lineHeight;
    style.letterSpacing = metrics.letterSpacing;
    style.description = `BAT ${role}; ${definition.font_weight}; ${definition.line_height}; ${definition.letter_spacing}`;
    result[role] = style;
  }
  return result;
}

/** @param {PluginAPI} figmaApi */
async function syncEffectStyles(figmaApi, manifest) {
  const styles = await figmaApi.getLocalEffectStylesAsync();
  const result = {};
  for (const [role, value] of Object.entries(manifest.theme.shadow.rollen)) {
    const name = `Shadow/${role.replace("_", "-")}`;
    let style = styles.find((candidate) => candidate.name === name);
    if (!style) {
      style = figmaApi.createEffectStyle();
      style.name = name;
      styles.push(style);
    }
    style.effects = parseCssShadow(value);
    style.description = `BAT shadow ${role}`;
    result[role.replace("_", "-")] = style;
  }
  return result;
}

/** @param {PluginAPI} figmaApi */
async function ensurePage(figmaApi, name) {
  let page = figmaApi.root.children.find((candidate) => candidate.name === name);
  if (!page) {
    page = figmaApi.createPage();
    page.name = name;
  }
  if (typeof page.loadAsync === "function") await page.loadAsync();
  return page;
}

/** @param {PluginAPI} figmaApi */
async function ensureSection(figmaApi, page, name) {
  let section = /** @type {SectionNode | undefined} */ (page.children.find(
    (candidate) => candidate.type === "SECTION" && candidate.name === name,
  ));
  if (!section) {
    section = figmaApi.createSection();
    section.name = name;
    page.appendChild(section);
  }
  return section;
}

/** @param {PluginAPI} figmaApi */
async function ensurePageLabel(figmaApi, page, name, description, snapshot, textStyle) {
  /** @type {FrameNode | undefined} */
  let frame = /** @type {FrameNode | undefined} */ (page.children.find(
    (node) => node.type === "FRAME" && node.name === "_Documentation",
  ));
  if (!frame) {
    frame = figmaApi.createFrame();
    frame.name = "_Documentation";
    page.appendChild(frame);
  }
  frame.layoutMode = "VERTICAL";
  frame.primaryAxisSizingMode = "AUTO";
  frame.counterAxisSizingMode = "FIXED";
  frame.resize(420, 120);
  frame.paddingTop = 24;
  frame.paddingBottom = 24;
  frame.paddingLeft = 24;
  frame.paddingRight = 24;
  frame.itemSpacing = 12;
  frame.fills = [];
  /** @type {TextNode[]} */
  const existing = /** @type {TextNode[]} */ (frame.children.filter(
    (child) => child.type === "TEXT" && child.name === "_GeneratedLabel",
  ));
  while (existing.length > 2) {
    const stale = existing.pop();
    if (stale) stale.remove();
  }
  const labels = [name, `${description}\n${snapshot}`];
  for (let index = 0; index < labels.length; index += 1) {
    let node = existing[index];
    if (!node) {
      node = figmaApi.createText();
      node.name = "_GeneratedLabel";
      frame.appendChild(node);
    }
    const font = textStyle.fontName;
    await figmaApi.loadFontAsync(font);
    node.fontName = font;
    node.fontSize = index === 0 ? Math.max(24, Number(textStyle.fontSize)) : 12;
    node.characters = labels[index];
  }
  return frame;
}

/** @param {PluginAPI} figmaApi */
function boundPaint(figmaApi, variable) {
  return figmaApi.variables.setBoundVariableForPaint(
    {type: "SOLID", color: {r: 0, g: 0, b: 0}}, "color", variable,
  );
}

function appearanceIndex(manifest) {
  return Object.fromEntries(manifest.appearances.map((appearance) => [appearance.id, appearance]));
}

/** @param {PluginAPI} figmaApi */
async function applyAppearance(figmaApi, node, appearance, refs, effectStyles) {
  if (!appearance) return;
  const roles = appearance.rollen;
  if (roles.material && refs.material[roles.material]) node.fills = [boundPaint(figmaApi, refs.material[roles.material])];
  if (roles.outline && refs.material[roles.outline]) node.strokes = [boundPaint(figmaApi, refs.material[roles.outline])];
  if (roles.border && refs.border[roles.border]) node.setBoundVariable("strokeWeight", refs.border[roles.border]);
  if (roles.radius && refs.radius[roles.radius]) {
    for (const property of ["topLeftRadius", "topRightRadius", "bottomLeftRadius", "bottomRightRadius"]) {
      node.setBoundVariable(property, refs.radius[roles.radius]);
    }
  }
  if (roles.spacing && refs.spacing[roles.spacing]) {
    for (const property of ["paddingTop", "paddingRight", "paddingBottom", "paddingLeft", "itemSpacing"]) {
      node.setBoundVariable(property, refs.spacing[roles.spacing]);
    }
  }
  if (roles.shadow && effectStyles[roles.shadow]) {
    await node.setEffectStyleIdAsync(effectStyles[roles.shadow].id);
  }
}

/** @param {PluginAPI} figmaApi */
async function syncComponentVariant(figmaApi, componentNode, definition, appearance, manifest, refs, textStyles, effectStyles) {
  componentNode.layoutMode = "VERTICAL";
  componentNode.primaryAxisSizingMode = "AUTO";
  componentNode.counterAxisSizingMode = "FIXED";
  componentNode.resize(280, Math.max(componentNode.height, 64));
  await applyAppearance(figmaApi, componentNode, appearance, refs, effectStyles);
  const foregroundRole = appearance && appearance.rollen.foreground;
  const foreground = foregroundRole ? refs.material[foregroundRole] : refs.palette.foreground;
  const typeRole = appearance && (appearance.rollen["label-style"] || appearance.rollen["body-style"]);
  const textStyle = textStyles[typeRole || "body"] || textStyles.body;
  for (const anatomy of definition.anatomie) {
    let text = componentNode.children.find((child) => child.type === "TEXT" && child.name === anatomy);
    if (!text) {
      text = figmaApi.createText();
      text.name = anatomy;
      componentNode.appendChild(text);
    }
    await figmaApi.loadFontAsync(textStyle.fontName);
    await text.setTextStyleIdAsync(textStyle.id);
    text.characters = anatomy;
    if (foreground) text.fills = [boundPaint(figmaApi, foreground)];
  }
  componentNode.description = `BAT component ${definition.id}; ${manifest.product.snapshot}`;
}

/** @param {PluginAPI} figmaApi */
async function syncComponents(figmaApi, manifest, refs, textStyles, effectStyles) {
  const appearances = appearanceIndex(manifest);
  const desired = desiredState(manifest);
  const page = await ensurePage(figmaApi, "Components");
  const result = {};
  let sectionY = 40;
  for (const definition of desired.components) {
    const section = await ensureSection(figmaApi, page, `Component / ${definition.naam}`);
    const labelFrame = await ensurePageLabel(figmaApi, section, definition.naam, `BAT component ${definition.id}`, desired.snapshot, textStyles.heading);
    labelFrame.x = 40;
    labelFrame.y = sectionY;
    /** @type {ComponentSetNode | undefined} */
    let componentSet = /** @type {ComponentSetNode | undefined} */ (section.children.find(
      (node) => node.type === "COMPONENT_SET" && node.name === definition.naam,
    ));
    const byName = new Map();
    if (componentSet) {
      for (const child of componentSet.children) byName.set(child.name, child);
    }
    const created = [];
    const refsForComponent = {};
    for (const variant of definition.figmaVariants) {
      const name = `Variant=${variant.profile}, State=${variant.state}`;
      let component = byName.get(name);
      if (!component) {
        component = figmaApi.createComponent();
        component.name = name;
        created.push(component);
      }
      await syncComponentVariant(
        figmaApi, component, definition, appearances[variant.appearance], manifest,
        refs, textStyles, effectStyles,
      );
      refsForComponent[`${variant.profile}:${variant.state}`] = component;
    }
    if (!componentSet) {
      if (!created.length) throw new Error(`Component '${definition.id}' has no Figma variants`);
      componentSet = figmaApi.combineAsVariants(created, section);
      componentSet.name = definition.naam;
    } else {
      for (const component of created) componentSet.appendChild(component);
    }
    componentSet.description = `${definition.doel || definition.naam}\nBAT ${definition.id}; ${desired.snapshot}`;
    const ordered = [...componentSet.children].sort((left, right) => left.name.localeCompare(right.name));
    const gap = manifest.theme.spacing ? px(manifest.theme.spacing.rollen.medium) : 16;
    let maxX = 0;
    let maxY = 0;
    for (let index = 0; index < ordered.length; index += 1) {
      const child = ordered[index];
      const column = index % 5;
      const row = Math.floor(index / 5);
      child.x = gap + column * (child.width + gap);
      child.y = gap + row * (child.height + gap);
      maxX = Math.max(maxX, child.x + child.width);
      maxY = Math.max(maxY, child.y + child.height);
    }
    componentSet.resizeWithoutConstraints(maxX + gap, maxY + gap);
    componentSet.x = 500;
    componentSet.y = sectionY;
    section.x = 40;
    section.y = sectionY;
    section.resizeWithoutConstraints(
      Math.max(componentSet.x + componentSet.width, labelFrame.x + labelFrame.width) + gap - section.x,
      Math.max(componentSet.height, labelFrame.height) + gap * 2,
    );
    sectionY += section.height + 120;
    result[definition.id] = {set: componentSet, variants: refsForComponent};
  }
  return result;
}

function svgForAsset(asset) {
  const [x, y, width, height] = asset.viewbox;
  const fill = asset.vulling || "none";
  const stroke = asset.lijn || "none";
  const strokeWidth = asset.lijndikte == null ? "" : ` stroke-width="${asset.lijndikte}"`;
  const linecap = asset.lijneinde ? ` stroke-linecap="${asset.lijneinde}"` : "";
  const linejoin = asset.lijnverbinding ? ` stroke-linejoin="${asset.lijnverbinding}"` : "";
  const paths = asset.paden.map((path) => `<path d="${path}"/>`).join("");
  return `<svg xmlns="http://www.w3.org/2000/svg" viewBox="${x} ${y} ${width} ${height}" fill="${fill}" stroke="${stroke}"${strokeWidth}${linecap}${linejoin}>${paths}</svg>`;
}

/** @param {PluginAPI} figmaApi */
async function syncAssets(figmaApi, manifest, textStyles) {
  const page = await ensurePage(figmaApi, "Assets & Surfaces");
  const section = await ensureSection(figmaApi, page, "Assets");
  const labelFrame = await ensurePageLabel(figmaApi, section, "Assets", `${manifest.assets.length} BAT vector assets`, manifest.product.snapshot, textStyles.heading);
  labelFrame.x = 40;
  labelFrame.y = 40;
  const result = {};
  let x = 500;
  let y = 40;
  let maxX = x;
  let maxY = y;
  for (const asset of manifest.assets) {
    const name = `Asset / ${asset.id}`;
    /** @type {ComponentNode | undefined} */
    let component = /** @type {ComponentNode | undefined} */ (section.children.find(
      (node) => node.type === "COMPONENT" && node.name === name,
    ));
    const marker = `BAT asset ${asset.id}; ${manifest.product.snapshot}`;
    if (!component) {
      component = figmaApi.createComponent();
      component.name = name;
      section.appendChild(component);
    }
    if (component.description !== marker) {
      for (const child of [...component.children]) child.remove();
      const imported = figmaApi.createNodeFromSvg(svgForAsset(asset));
      for (const child of [...imported.children]) component.appendChild(child);
      imported.remove();
      const width = Math.max(1, asset.viewbox[2]);
      const height = Math.max(1, asset.viewbox[3]);
      component.resizeWithoutConstraints(width, height);
      component.description = marker;
    }
    component.x = x;
    component.y = y;
    maxX = Math.max(maxX, x + component.width);
    x += component.width + 48;
    if (x > 1800) {
      x = 500;
      y += 420;
    }
    maxY = Math.max(maxY, y + 420);
    result[asset.id] = component;
  }
  section.x = 40;
  section.y = 40;
  section.resizeWithoutConstraints(
    Math.max(maxX + 48, labelFrame.x + labelFrame.width) - section.x,
    Math.max(maxY, labelFrame.y + labelFrame.height + 40) - section.y,
  );
  return result;
}

function matchingComposition(layout, compositions) {
  const layoutInstances = [...layout.regions.map((region) => region.instance)].sort();
  const matches = compositions.filter((composition) => {
    const compositionInstances = [...composition.instances.map((instance) => instance.id)].sort();
    return JSON.stringify(compositionInstances) === JSON.stringify(layoutInstances);
  });
  if (matches.length !== 1) {
    throw new Error(`Layout '${layout.id}' must map to exactly one composition`);
  }
  return matches[0];
}

function componentForInstance(componentRefs, instance) {
  const ref = componentRefs[instance.component];
  if (!ref) throw new Error(`Missing Figma component '${instance.component}'`);
  const key = `${instance.variant || "base"}:rest`;
  const component = ref.variants[key];
  if (!component) throw new Error(`Missing Figma variant '${instance.component}' '${key}'`);
  return component;
}

/** @param {PluginAPI} figmaApi */
async function syncSurfaces(figmaApi, manifest, refs, componentRefs, textStyles) {
  const page = await ensurePage(figmaApi, "Assets & Surfaces");
  /** @type {SectionNode | undefined} */
  const assetsSection = /** @type {SectionNode | undefined} */ (page.children.find(
    (node) => node.type === "SECTION" && node.name === "Assets",
  ));
  const baseY = assetsSection ? assetsSection.y + assetsSection.height + 120 : 40;
  const section = await ensureSection(figmaApi, page, "Surfaces");
  const labelFrame = await ensurePageLabel(figmaApi, section, "Surfaces", `${manifest.layouts.length} native BAT layouts`, manifest.product.snapshot, textStyles.heading);
  labelFrame.x = 40;
  labelFrame.y = baseY;
  const gap = px(manifest.theme.spacing.rollen.medium);
  let surfaceY = baseY + 180;
  const result = {};
  for (const layout of manifest.layouts) {
    const composition = matchingComposition(layout, manifest.compositions);
    const name = `Surface / ${layout.id}`;
    /** @type {FrameNode | undefined} */
    let frame = /** @type {FrameNode | undefined} */ (section.children.find(
      (node) => node.type === "FRAME" && node.name === name,
    ));
    if (!frame) {
      frame = figmaApi.createFrame();
      frame.name = name;
      section.appendChild(frame);
    }
    /** @type {Record<string, InstanceNode>} */
    const instances = {};
    for (const instance of composition.instances) {
      const target = componentForInstance(componentRefs, instance);
      const named = frame.children.find((child) => child.name === instance.id);
      if (named && named.type !== "INSTANCE") {
        throw new Error(`Surface '${layout.id}' contains incompatible node '${instance.id}'`);
      }
      const node = named || target.createInstance();
      if (node.type !== "INSTANCE") throw new Error(`Surface '${layout.id}' requires Figma instances`);
      if (!named) {
        node.name = instance.id;
        frame.appendChild(node);
      } else {
        node.swapComponent(target);
      }
      instances[instance.id] = node;
    }
    if (layout.type === "grid") {
      const cellWidth = Math.max(...Object.values(instances).map((node) => node.width));
      const cellHeight = Math.max(...Object.values(instances).map((node) => node.height));
      for (const region of layout.regions) {
        const node = instances[region.instance];
        node.x = gap + (region.column - 1) * (cellWidth + gap);
        node.y = gap + (region.row - 1) * (cellHeight + gap);
        node.resizeWithoutConstraints(
          cellWidth * region.column_span + gap * (region.column_span - 1),
          cellHeight * region.row_span + gap * (region.row_span - 1),
        );
      }
      frame.resizeWithoutConstraints(
        gap + layout.columns * (cellWidth + gap),
        gap + layout.rows * (cellHeight + gap),
      );
    } else {
      frame.layoutMode = layout.direction === "horizontal" ? "HORIZONTAL" : "VERTICAL";
      frame.primaryAxisSizingMode = "AUTO";
      frame.counterAxisSizingMode = "AUTO";
      frame.itemSpacing = gap;
      frame.paddingTop = gap;
      frame.paddingRight = gap;
      frame.paddingBottom = gap;
      frame.paddingLeft = gap;
    }
    if (refs.material.canvas) frame.fills = [boundPaint(figmaApi, refs.material.canvas)];
    frame.x = 40;
    frame.y = surfaceY;
    surfaceY += frame.height + 120;
    result[layout.id] = frame;
  }
  section.x = 40;
  section.y = baseY;
  section.resizeWithoutConstraints(
    Math.max(labelFrame.x + labelFrame.width, 900) - section.x,
    surfaceY - baseY,
  );
  return result;
}

/** @param {PluginAPI} figmaApi */
async function syncFileStructure(figmaApi, manifest, refs, textStyles) {
  const page = await ensurePage(figmaApi, "Foundations");
  let sectionY = 40;

  const cover = await ensureSection(figmaApi, page, "Cover");
  const coverFrame = await ensurePageLabel(
    figmaApi, cover, manifest.figma_master.naam, manifest.figma_master.doel,
    manifest.product.snapshot, textStyles.title,
  );
  coverFrame.x = 40;
  coverFrame.y = sectionY;
  if (refs.material.canvas) coverFrame.fills = [boundPaint(figmaApi, refs.material.canvas)];
  cover.x = 40;
  cover.y = sectionY;
  cover.resizeWithoutConstraints(Math.max(coverFrame.width, 480) + 80, coverFrame.height + 80);
  sectionY += cover.height + 80;

  const gettingStarted = await ensureSection(figmaApi, page, "Getting Started");
  const gettingStartedFrame = await ensurePageLabel(
    figmaApi, gettingStarted, "Getting Started",
    `Generated from ${manifest.product.id} ${manifest.product.snapshot}`,
    manifest.product.snapshot, textStyles.heading,
  );
  gettingStartedFrame.x = 40;
  gettingStartedFrame.y = sectionY;
  gettingStarted.x = 40;
  gettingStarted.y = sectionY;
  gettingStarted.resizeWithoutConstraints(Math.max(gettingStartedFrame.width, 480) + 80, gettingStartedFrame.height + 80);
  sectionY += gettingStarted.height + 80;

  const foundations = await ensureSection(figmaApi, page, "Foundations");
  const foundationFrame = await ensurePageLabel(
    figmaApi, foundations, "Foundations",
    "Color primitives, semantic colors, spacing, radius, borders, motion, typography and shadows are native Figma foundations.",
    manifest.product.snapshot, textStyles.heading,
  );
  foundationFrame.x = 40;
  foundationFrame.y = sectionY;
  if (refs.material.surface) foundationFrame.fills = [boundPaint(figmaApi, refs.material.surface)];
  foundations.x = 40;
  foundations.y = sectionY;
  foundations.resizeWithoutConstraints(Math.max(foundationFrame.width, 480) + 80, foundationFrame.height + 80);
}

function assertExactNames(kind, actual, expected) {
  const normalizedActual = [...actual].sort();
  const normalizedExpected = [...expected].sort();
  if (JSON.stringify(normalizedActual) !== JSON.stringify(normalizedExpected)) {
    throw new Error(
      `${kind} mismatch: expected ${JSON.stringify(normalizedExpected)}, got ${JSON.stringify(normalizedActual)}`,
    );
  }
}

/** @param {PluginAPI} figmaApi */
async function exactPage(figmaApi, name) {
  const pages = figmaApi.root.children.filter((page) => page.name === name);
  if (pages.length !== 1) {
    throw new Error(`Expected exactly one Figma page '${name}', got ${pages.length}`);
  }
  const page = pages[0];
  if (typeof page.loadAsync === "function") await page.loadAsync();
  return page;
}

/** @param {PluginAPI} figmaApi */
async function exactSection(figmaApi, pageName, sectionName) {
  const page = await exactPage(figmaApi, pageName);
  const sections = page.children.filter(
    (node) => node.type === "SECTION" && node.name === sectionName,
  );
  if (sections.length !== 1) {
    throw new Error(`Expected exactly one Figma section '${sectionName}' on page '${pageName}', got ${sections.length}`);
  }
  return sections[0];
}

function normalizedVariableValue(value) {
  if (value && typeof value === "object" && value.type === "VARIABLE_ALIAS") {
    return {type: value.type, id: value.id};
  }
  if (value && typeof value === "object") {
    return Object.fromEntries(Object.entries(value).sort(([left], [right]) => left.localeCompare(right)));
  }
  return value;
}

/** @param {PluginAPI} figmaApi */
async function verifyLiveState(figmaApi, manifest) {
  const desired = desiredState(manifest);
  const collections = await figmaApi.variables.getLocalVariableCollectionsAsync();
  const variables = await figmaApi.variables.getLocalVariablesAsync();
  const managedCollections = [];
  for (const [key, name] of Object.entries(COLLECTION_NAMES)) {
    const matches = collections.filter((collection) => collection.name === name);
    if (matches.length !== 1) {
      throw new Error(`Expected exactly one variable collection '${name}', got ${matches.length}`);
    }
    const collection = matches[0];
    if (collection.modes.length !== 1 || collection.modes[0].name !== "Value") {
      throw new Error(`Variable collection '${name}' must have exactly one 'Value' mode`);
    }
    const owned = variables
      .filter((variable) => variable.variableCollectionId === collection.id)
      .sort((left, right) => left.name.localeCompare(right.name));
    if (owned.length !== desired.collections[key]) {
      throw new Error(
        `Variable collection '${name}' expected ${desired.collections[key]} variables, got ${owned.length}`,
      );
    }
    const modeId = collection.modes[0].modeId;
    managedCollections.push({
      name,
      variables: owned.map((variable) => ({
        id: variable.id,
        name: variable.name,
        type: variable.resolvedType,
        scopes: [...variable.scopes].sort(),
        web: variable.codeSyntax.WEB || null,
        value: normalizedVariableValue(variable.valuesByMode[modeId]),
      })),
    });
  }

  const localTextStyles = await figmaApi.getLocalTextStylesAsync();
  const textStyleNames = desired.textStyles.map((role) => `Type/${role}`);
  const textStyles = localTextStyles.filter((style) => textStyleNames.includes(style.name));
  assertExactNames("Text styles", textStyles.map((style) => style.name), textStyleNames);
  const textStyleState = textStyles
    .map((style) => ({
      id: style.id,
      name: style.name,
      fontName: style.fontName,
      fontSize: style.fontSize,
      lineHeight: style.lineHeight,
      letterSpacing: style.letterSpacing,
      description: style.description,
    }))
    .sort((left, right) => left.name.localeCompare(right.name));

  const localEffectStyles = await figmaApi.getLocalEffectStylesAsync();
  const effectStyleNames = desired.effectStyles.map((role) => `Shadow/${role.replace("_", "-")}`);
  const effectStyles = localEffectStyles.filter((style) => effectStyleNames.includes(style.name));
  assertExactNames("Effect styles", effectStyles.map((style) => style.name), effectStyleNames);
  const effectStyleState = effectStyles
    .map((style) => ({id: style.id, name: style.name, effects: style.effects, description: style.description}))
    .sort((left, right) => left.name.localeCompare(right.name));

  const componentState = [];
  for (const definition of desired.components) {
    const section = await exactSection(figmaApi, "Components", `Component / ${definition.naam}`);
    const sets = /** @type {ComponentSetNode[]} */ (section.children.filter(
      (node) => node.type === "COMPONENT_SET" && node.name === definition.naam,
    ));
    if (sets.length !== 1) {
      throw new Error(`Component '${definition.id}' expected exactly one component set, got ${sets.length}`);
    }
    const set = sets[0];
    const expectedVariants = definition.figmaVariants.map(
      (variant) => `Variant=${variant.profile}, State=${variant.state}`,
    );
    assertExactNames(
      `Component '${definition.id}' variants`,
      set.children.map((child) => child.name),
      expectedVariants,
    );
    if (!set.description.includes(desired.snapshot)) {
      throw new Error(`Component '${definition.id}' does not carry snapshot '${desired.snapshot}'`);
    }
    for (const child of set.children) {
      if (child.type !== "COMPONENT" || !child.description.includes(desired.snapshot)) {
        throw new Error(`Component '${definition.id}' contains an unverified variant '${child.name}'`);
      }
    }
    componentState.push({
      id: set.id,
      name: definition.id,
      variants: [...set.children].map((child) => ({id: child.id, name: child.name})).sort(
        (left, right) => left.name.localeCompare(right.name),
      ),
    });
  }

  const assetsSection = await exactSection(figmaApi, "Assets & Surfaces", "Assets");
  const assetNames = desired.assets.map((id) => `Asset / ${id}`);
  const assetNodes = /** @type {ComponentNode[]} */ (assetsSection.children.filter(
    (node) => node.type === "COMPONENT" && assetNames.includes(node.name),
  ));
  assertExactNames("Assets", assetNodes.map((node) => node.name), assetNames);
  for (const node of assetNodes) {
    if (!node.description.includes(desired.snapshot)) {
      throw new Error(`Asset '${node.name}' does not carry snapshot '${desired.snapshot}'`);
    }
  }
  const assetState = assetNodes
    .map((node) => ({id: node.id, name: node.name, width: node.width, height: node.height, children: node.children.length}))
    .sort((left, right) => left.name.localeCompare(right.name));

  const surfacesSection = await exactSection(figmaApi, "Assets & Surfaces", "Surfaces");
  const surfaceNames = desired.layouts.map((id) => `Surface / ${id}`);
  const surfaceNodes = /** @type {FrameNode[]} */ (surfacesSection.children.filter(
    (node) => node.type === "FRAME" && surfaceNames.includes(node.name),
  ));
  assertExactNames("Surfaces", surfaceNodes.map((node) => node.name), surfaceNames);
  const surfaceState = surfaceNodes
    .map((node) => ({
      id: node.id,
      name: node.name,
      width: node.width,
      height: node.height,
      instances: /** @type {InstanceNode[]} */ (node.children
        .filter((child) => child.type === "INSTANCE"))
        .map((child) => ({id: child.id, name: child.name, mainComponent: child.mainComponent && child.mainComponent.id}))
        .sort((left, right) => left.name.localeCompare(right.name)),
    }))
    .sort((left, right) => left.name.localeCompare(right.name));

  const documentedSections = [
    {page: "Foundations", section: "Cover"},
    {page: "Foundations", section: "Getting Started"},
    {page: "Foundations", section: "Foundations"},
    {page: "Assets & Surfaces", section: "Assets"},
    {page: "Assets & Surfaces", section: "Surfaces"},
  ];
  for (const {page: pageName, section: sectionName} of documentedSections) {
    const section = await exactSection(figmaApi, pageName, sectionName);
    const documentation = /** @type {FrameNode | undefined} */ (section.children.find(
      (node) => node.type === "FRAME" && node.name === "_Documentation",
    ));
    const labels = documentation && /** @type {TextNode[]} */ (documentation.children.filter(
      (child) => child.type === "TEXT" && child.name === "_GeneratedLabel",
    ));
    if (!labels || !labels.some((label) => label.characters.includes(desired.snapshot))) {
      throw new Error(`Section '${sectionName}' on page '${pageName}' does not document snapshot '${desired.snapshot}'`);
    }
  }

  return {
    snapshot: desired.snapshot,
    collections: managedCollections,
    textStyles: textStyleState,
    effectStyles: effectStyleState,
    components: componentState,
    assets: assetState,
    surfaces: surfaceState,
  };
}

/** @param {PluginAPI} figmaApi */
async function runSync(figmaApi, manifest) {
  assertManifest(manifest);
  const foundations = await syncFoundations(figmaApi, manifest);
  const textStyles = await syncTextStyles(figmaApi, manifest);
  const effectStyles = await syncEffectStyles(figmaApi, manifest);
  await syncFileStructure(figmaApi, manifest, foundations.refs, textStyles);
  const componentRefs = await syncComponents(
    figmaApi, manifest, foundations.refs, textStyles, effectStyles,
  );
  await syncAssets(figmaApi, manifest, textStyles);
  await syncSurfaces(figmaApi, manifest, foundations.refs, componentRefs, textStyles);
  const plan = desiredState(manifest);
  return {
    snapshot: plan.snapshot,
    collections: Object.keys(plan.collections).length,
    variables: Object.values(plan.collections).reduce((sum, value) => sum + value, 0),
    textStyles: plan.textStyles.length,
    effectStyles: plan.effectStyles.length,
    assets: plan.assets.length,
    componentFamilies: plan.components.length,
    figmaVariants: plan.components.reduce((sum, component) => sum + component.figmaVariants.length, 0),
    surfaces: plan.layouts.length,
  };
}

/** @param {PluginAPI} figmaApi */
async function runVerifiedSync(figmaApi, manifest) {
  const firstSummary = await runSync(figmaApi, manifest);
  const firstState = await verifyLiveState(figmaApi, manifest);
  const secondSummary = await runSync(figmaApi, manifest);
  const secondState = await verifyLiveState(figmaApi, manifest);
  if (JSON.stringify(firstState) !== JSON.stringify(secondState)) {
    throw new Error("Second Figma sync changed managed state; adapter is not idempotent");
  }
  return {...secondSummary, verified: true, idempotent: true, firstSummary};
}

if (typeof figma !== "undefined") {
  runVerifiedSync(figma, BP_MANIFEST)
    .then((summary) => figma.closePlugin(
      `Beckeringh Palace verified ${summary.variables} variables, ${summary.componentFamilies} component families, ${summary.assets} assets and ${summary.surfaces} surfaces; second sync is idempotent.`,
    ))
    .catch((error) => figma.closePlugin(`Beckeringh Palace sync failed: ${error.message}`));
}

if (typeof module !== "undefined" && module.exports) {
  module.exports = {
    manifest: BP_MANIFEST,
    assertManifest,
    desiredState,
    parseCssShadow,
    runSync,
    verifyLiveState,
    runVerifiedSync,
  };
}
