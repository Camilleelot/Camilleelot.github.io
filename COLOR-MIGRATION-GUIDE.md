# Color System Migration Guide

## Summary

This guide shows how to migrate from the current inconsistent color palette to the new unified Edward Tufte-inspired system.

## New Color System

### The Palette

| Color | Light Mode | Dark Mode | Use Case |
|-------|------------|-----------|----------|
| **Primary (Slate Blue)** | `#2c4f6b` | `#6b9bd9` | Research, publications, headings, main CTAs |
| **Secondary (Burnt Sienna)** | `#a0522d` | `#d9865a` | Tools, interactive elements, data viz |
| **Accent (Burgundy)** | `#8b3a3a` | `#c97a7a` | Key findings, emphasis, warnings |
| **Success (Sage Green)** | `#5a6d5a` | `#7a9d7a` | Positive states, confirmations |

### CSS Variables

```css
--color-primary     /* Slate blue */
--color-secondary   /* Burnt sienna */
--color-accent      /* Burgundy */
--color-success     /* Sage green */
--color-text-muted  /* Gray for secondary text */
--color-bg-card     /* Card backgrounds */
--color-gray-200    /* Borders and dividers */
```

---

## Page-by-Page Migration

### 1. Fleet Management Pages

**Files:**
- `fleet-management/index.html`
- `fleet-management/deployment-guide.html`
- `fleet-management/technical-walkthrough.html`

**Current Colors:**
- Primary: `#2c5282`, `#3182ce` (blues)
- Accent: `#48bb78` (green), `#ed8936` (orange)

**Replacements:**
```css
/* OLD → NEW */
#2c5282 → var(--color-primary)
#3182ce → var(--color-primary)
#5a7fb8 → var(--color-primary)  /* dark mode variant */
#6b9bd1 → var(--color-primary)  /* dark mode variant */

#48bb78 → var(--color-success)
#ed8936 → var(--color-secondary)
```

**Specific Changes:**

1. **Feature boxes** - Change border-left from `#2c5282` to `var(--color-primary)`
2. **CTA buttons** - Use `.cta-button` class (already defined in colors.css)
3. **Success callouts** - Change from `#48bb78` to `var(--color-success)`
4. **Warning callouts** - Change from `#ed8936` to `var(--color-secondary)`
5. **Headings with color** - Use `var(--color-primary)` instead of `#2c5282`

---

### 2. Calgary Rezoning / Publications

**Files:**
- `CalgaryRezoningProject.html`
- `papers/calgary-rezoning/v1.0/index.html`

**Current Colors:**
- Emphasis: `#cc0000` (bright red)
- Secondary: `#4a5a8a` (muted blue), `#6b8e6b` (muted green)

**Replacements:**
```css
/* OLD → NEW */
#cc0000 → var(--color-accent)   /* Key findings, emphasis */
#4a5a8a → var(--color-primary)  /* Charts, data viz */
#6b8e6b → var(--color-success)  /* Positive data points */
```

**Specific Changes:**

1. **Key finding text** - Change `.emphasis` class from `#cc0000` to `var(--color-accent)`
2. **Data visualization colors:**
   ```javascript
   // In JavaScript chart config:
   accentColor: 'var(--color-accent)'     // was #cc0000
   mutedBlue: 'var(--color-primary)'      // was #4a5a8a
   mutedGreen: 'var(--color-success)'     // was #6b8e6b
   ```
3. **Callout boxes** - Use `.card-policy` class for key finding boxes
4. **Chart borders** - Use `var(--color-accent)` for emphasis lines

**Note:** The bright red `#cc0000` is too saturated for Tufte style. The burgundy `#8b3a3a` maintains emphasis while being more muted.

---

### 3. Turnover Analysis Tool

**File:** `turnover-analysis.html`

**Current Colors:**
- Green: `#2d5016`, `#3d6826`

**Replacements:**
```css
/* OLD → NEW */
#2d5016 → var(--color-success)
#3d6826 → var(--color-success)
```

**Specific Changes:**

1. **CTA buttons** - Already dark green, map to `var(--color-success)` or use `.cta-button`
2. **Tool card** - Use `.card-tool` class with `var(--color-secondary)` border

---

### 4. Scrollytelling Demo

**File:** `scrollytelling-demo.html`

**Current Colors:**
- Progress bar: `#ff6b35` (orange)
- Various gradients (purple, pink, cyan, etc.)

**Replacements:**
```css
/* OLD → NEW */
#ff6b35 → var(--color-secondary)  /* Progress bar, accents */

/* Simplify gradients to solid colors */
/* Remove: #667eea, #764ba2, #f093fb, #f5576c, #4facfe, #00f2fe, #43e97b, #38f9d7, #fa709a, #fee140 */
```

**Specific Changes:**

1. **Progress bar** - Change from `#ff6b35` to `var(--color-secondary)`
2. **Step indicators** - Replace colorful gradients with single muted colors from the palette
3. **Active step highlight** - Use `var(--color-primary)` with opacity
4. **Chart accents** - Use `var(--color-accent)` for emphasis points

**Philosophy:** Tufte would not approve of rainbow gradients. Replace with subtle opacity changes and single accent colors.

---

### 5. Papers Index / Publications Hub

**File:** `papers/index.html`

**Current Colors:**
- Badges: Multiple backgrounds (slate, green, tan)
- Various card borders

**Replacements:**
```css
/* Badge backgrounds */
.badge { background: var(--color-gray-200); }  /* Neutral */

/* Semantic badges */
POLICY ANALYSIS → .badge-research (--color-primary)
DATA REPOSITORY → .badge-tool (--color-success)
INTERACTIVE TOOL → .badge-tool (--color-secondary)
```

**Specific Changes:**

1. **Publication cards** - Use `.card-research` class
2. **Stat boxes** - Keep neutral with `var(--color-bg-card)` background
3. **Badges:**
   - Policy Analysis → `.badge-research`
   - Data Repository → `.badge-tool` with success color
   - Tools → `.badge-tool`

---

## Global Changes (All Pages)

### 1. Add CSS Import

Add to `<head>` of every page (after `tufte.css`):

```html
<link rel="stylesheet" href="/colors.css">
```

Or if in subdirectory:

```html
<link rel="stylesheet" href="../colors.css">
```

### 2. Update Inline Styles

**Before:**
```html
<div style="background: #f8f9fa; border-left: 4px solid #2c5282;">
```

**After:**
```html
<div style="background: var(--color-bg-card); border-left: 4px solid var(--color-primary);">
```

Or better, use semantic classes:
```html
<div class="card-research">
```

### 3. Update JavaScript Chart Colors

**Before:**
```javascript
const colors = {
  backgroundColor: '#fffff8',
  accentColor: '#cc0000',
  mutedBlue: '#4a5a8a'
};
```

**After:**
```javascript
const colors = {
  backgroundColor: 'var(--color-bg)',
  accentColor: 'var(--color-accent)',
  primaryColor: 'var(--color-primary)'
};
```

**Note:** For Canvas/JavaScript rendering, you may need to get computed values:

```javascript
const root = document.documentElement;
const primaryColor = getComputedStyle(root).getPropertyValue('--color-primary').trim();
```

---

## Testing Checklist

After migrating each page:

- [ ] Add `colors.css` import to `<head>`
- [ ] Replace all hardcoded hex colors with CSS variables
- [ ] Use semantic classes where applicable (`.card-research`, `.cta-button`, etc.)
- [ ] Test in **light mode**
- [ ] Test in **dark mode** (toggle system preference)
- [ ] Check all interactive states (hover, focus)
- [ ] Verify WCAG contrast ratios
- [ ] Check data visualizations/charts render correctly
- [ ] Validate that emphasis text is still visible

---

## Quick Reference: Old → New Mapping

| Old Color | Hex | New Variable | New Hex (Light) |
|-----------|-----|--------------|-----------------|
| Fleet Blue | `#2c5282` | `--color-primary` | `#2c4f6b` |
| Fleet Blue Alt | `#3182ce` | `--color-primary` | `#2c4f6b` |
| Calgary Red | `#cc0000` | `--color-accent` | `#8b3a3a` |
| Turnover Green | `#2d5016` | `--color-success` | `#5a6d5a` |
| Scrollytelling Orange | `#ff6b35` | `--color-secondary` | `#a0522d` |
| Fleet Green | `#48bb78` | `--color-success` | `#5a6d5a` |
| Fleet Orange | `#ed8936` | `--color-secondary` | `#a0522d` |

---

## Benefits of Migration

1. **Consistency** - All pages use the same semantic color system
2. **Maintenance** - Change colors globally by updating `colors.css`
3. **Dark Mode** - Automatic light/dark mode adaptation
4. **Accessibility** - All colors tested for WCAG AA contrast
5. **Tufte-compliant** - Muted, purposeful colors that don't distract
6. **Semantic** - Color meanings are clear (primary = research, secondary = tools, etc.)

---

## Next Steps

1. Start with the most visible page (`index.html`)
2. Migrate one section at a time
3. Test in both light and dark modes
4. Move to fleet-management pages (most color-heavy)
5. Update Calgary rezoning (requires chart color updates)
6. Simplify scrollytelling gradients
7. Standardize publication badges

---

## Reference

- **Color System Documentation:** `/color-reference.html`
- **CSS Variables File:** `/colors.css`
- **Original Tufte CSS:** `/tufte.css` (unchanged)
