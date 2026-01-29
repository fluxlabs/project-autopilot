---
name: accessibility
description: WCAG guidelines, accessibility testing patterns, and a11y best practices. Reference this skill when auditing accessibility.
---

# Accessibility Skill
# Project Autopilot - WCAG guidelines and patterns
# Copyright (c) 2026 Jeremy McSpadden <jeremy@fluxlabs.net>

Comprehensive accessibility patterns for WCAG compliance.

---

## WCAG Quick Reference

### Principles (POUR)

| Principle | Description |
|-----------|-------------|
| **Perceivable** | Info must be presentable in ways users can perceive |
| **Operable** | UI components must be operable |
| **Understandable** | Info and UI operation must be understandable |
| **Robust** | Content must be robust enough for assistive tech |

### Conformance Levels

| Level | Description | Typical Target |
|-------|-------------|----------------|
| A | Minimum | Basic compliance |
| AA | Standard | **Most projects** |
| AAA | Enhanced | Specialized needs |

---

## Common Patterns

### Images

```tsx
// Informative image
<img
  src="/product.jpg"
  alt="Red leather wallet with brass clasp"
/>

// Decorative image
<img
  src="/divider.svg"
  alt=""
  role="presentation"
/>

// Complex image with long description
<figure>
  <img
    src="/chart.png"
    alt="Q4 sales chart showing 25% growth"
    aria-describedby="chart-desc"
  />
  <figcaption id="chart-desc">
    Detailed description of the data...
  </figcaption>
</figure>
```

### Forms

```tsx
// Proper labeling
<div className="form-group">
  <label htmlFor="email">Email Address</label>
  <input
    id="email"
    type="email"
    aria-describedby="email-hint email-error"
    aria-invalid={hasError}
    required
  />
  <span id="email-hint" className="hint">
    We'll never share your email
  </span>
  {hasError && (
    <span id="email-error" className="error" role="alert">
      Please enter a valid email
    </span>
  )}
</div>

// Group related inputs
<fieldset>
  <legend>Shipping Address</legend>
  <label htmlFor="street">Street</label>
  <input id="street" type="text" />
  <label htmlFor="city">City</label>
  <input id="city" type="text" />
</fieldset>
```

### Buttons and Links

```tsx
// Button vs Link
// Button: Performs an action
<button type="button" onClick={handleSave}>
  Save Changes
</button>

// Link: Navigates somewhere
<a href="/products">View Products</a>

// Icon-only button
<button
  type="button"
  aria-label="Close dialog"
  onClick={handleClose}
>
  <XIcon aria-hidden="true" />
</button>

// Button with loading state
<button
  type="submit"
  aria-busy={isLoading}
  disabled={isLoading}
>
  {isLoading ? (
    <>
      <Spinner aria-hidden="true" />
      <span className="sr-only">Saving...</span>
    </>
  ) : (
    'Save'
  )}
</button>
```

### Navigation

```tsx
// Skip link
<a href="#main-content" className="skip-link">
  Skip to main content
</a>

// Main navigation
<nav aria-label="Main navigation">
  <ul>
    <li><a href="/" aria-current="page">Home</a></li>
    <li><a href="/products">Products</a></li>
    <li><a href="/about">About</a></li>
  </ul>
</nav>

// Breadcrumbs
<nav aria-label="Breadcrumb">
  <ol>
    <li><a href="/">Home</a></li>
    <li><a href="/products">Products</a></li>
    <li aria-current="page">Widget Pro</li>
  </ol>
</nav>

// Skip link CSS
.skip-link {
  position: absolute;
  left: -9999px;
  z-index: 9999;
}

.skip-link:focus {
  left: 10px;
  top: 10px;
  padding: 1rem;
  background: white;
}
```

### Modals and Dialogs

```tsx
// Accessible modal
function Modal({ isOpen, onClose, title, children }) {
  const modalRef = useRef(null);

  useEffect(() => {
    if (isOpen) {
      // Trap focus
      modalRef.current?.focus();

      // Handle escape key
      const handleEscape = (e) => {
        if (e.key === 'Escape') onClose();
      };
      document.addEventListener('keydown', handleEscape);

      return () => {
        document.removeEventListener('keydown', handleEscape);
      };
    }
  }, [isOpen, onClose]);

  if (!isOpen) return null;

  return (
    <div
      role="dialog"
      aria-modal="true"
      aria-labelledby="modal-title"
      ref={modalRef}
      tabIndex={-1}
    >
      <h2 id="modal-title">{title}</h2>
      {children}
      <button onClick={onClose}>Close</button>
    </div>
  );
}
```

### Tables

```tsx
// Accessible data table
<table>
  <caption>Q4 2025 Sales by Region</caption>
  <thead>
    <tr>
      <th scope="col">Region</th>
      <th scope="col">Q4 Sales</th>
      <th scope="col">Growth</th>
    </tr>
  </thead>
  <tbody>
    <tr>
      <th scope="row">North America</th>
      <td>$1.2M</td>
      <td>+15%</td>
    </tr>
    <tr>
      <th scope="row">Europe</th>
      <td>$890K</td>
      <td>+22%</td>
    </tr>
  </tbody>
</table>
```

### Live Regions

```tsx
// Status messages
<div role="status" aria-live="polite">
  {saveStatus === 'saving' && 'Saving...'}
  {saveStatus === 'saved' && 'Changes saved!'}
</div>

// Error alerts
<div role="alert" aria-live="assertive">
  {error && `Error: ${error.message}`}
</div>

// Loading indicator
<div aria-live="polite" aria-busy={isLoading}>
  {isLoading ? 'Loading content...' : 'Content loaded'}
</div>
```

---

## Color Contrast

### Minimum Ratios

| Text Type | Level AA | Level AAA |
|-----------|----------|-----------|
| Normal text | 4.5:1 | 7:1 |
| Large text (18pt+) | 3:1 | 4.5:1 |
| UI components | 3:1 | 3:1 |

### Color Combinations

```css
/* Good contrasts (AA compliant) */
.good-contrast {
  /* Dark text on light background */
  color: #333333;           /* 12.6:1 on white */
  background: #ffffff;

  /* Light text on dark background */
  color: #ffffff;
  background: #333333;
}

/* Bad contrasts (fail AA) */
.bad-contrast {
  color: #888888;           /* 3.5:1 on white - fails */
  background: #ffffff;

  color: #757575;           /* 4.6:1 - barely passes */
}

/* Don't rely on color alone */
.error {
  color: #d32f2f;           /* Red */
  border-left: 3px solid;   /* Also has visual indicator */
}

.error::before {
  content: "⚠ ";            /* Also has icon */
}
```

---

## Keyboard Navigation

### Focus Management

```css
/* Visible focus indicator */
:focus {
  outline: 2px solid #005fcc;
  outline-offset: 2px;
}

/* Skip default outline only if custom provided */
:focus-visible {
  outline: 3px solid #005fcc;
  outline-offset: 2px;
}

/* Focus within for containers */
.card:focus-within {
  box-shadow: 0 0 0 3px #005fcc;
}
```

### Tab Order

```tsx
// Natural tab order (follows DOM)
<header>
  <nav>...</nav>
</header>
<main>
  <form>
    <input tabIndex={0} />  {/* Default, follows DOM */}
    <input tabIndex={0} />
    <button tabIndex={0}>Submit</button>
  </form>
</main>

// Remove from tab order (but still focusable via JS)
<div tabIndex={-1} ref={focusTarget}>
  Focus will be moved here programmatically
</div>

// Never use tabIndex > 0
// ❌ <input tabIndex={5} />
```

### Keyboard Patterns

| Component | Keys |
|-----------|------|
| Button | Enter, Space |
| Link | Enter |
| Checkbox | Space |
| Radio | Arrow keys |
| Dropdown | Arrow keys, Enter, Escape |
| Dialog | Escape to close |
| Tabs | Arrow keys, Home, End |

---

## Screen Reader Patterns

### Visually Hidden Content

```css
/* Screen reader only (visually hidden) */
.sr-only {
  position: absolute;
  width: 1px;
  height: 1px;
  padding: 0;
  margin: -1px;
  overflow: hidden;
  clip: rect(0, 0, 0, 0);
  white-space: nowrap;
  border: 0;
}

/* Focusable when reached */
.sr-only-focusable:focus {
  position: static;
  width: auto;
  height: auto;
  margin: 0;
  overflow: visible;
  clip: auto;
  white-space: normal;
}
```

### ARIA Usage

```tsx
// States
<button aria-pressed={isActive}>Toggle</button>
<input aria-invalid={hasError} />
<section aria-expanded={isOpen}>...</section>

// Relationships
<input aria-describedby="hint" />
<span id="hint">Helpful text</span>

<button aria-controls="menu">Menu</button>
<ul id="menu">...</ul>

// Landmarks
<header role="banner">...</header>
<nav role="navigation">...</nav>
<main role="main">...</main>
<footer role="contentinfo">...</footer>
```

---

## Testing Checklist

### Manual Testing

- [ ] Navigate with keyboard only
- [ ] Test with screen reader (VoiceOver, NVDA)
- [ ] Zoom to 200%
- [ ] Check color contrast
- [ ] Verify focus indicators
- [ ] Test without CSS
- [ ] Check heading hierarchy

### Automated Testing

```typescript
// Jest + jest-axe
import { axe, toHaveNoViolations } from 'jest-axe';

expect.extend(toHaveNoViolations);

test('component has no accessibility violations', async () => {
  const { container } = render(<MyComponent />);
  const results = await axe(container);
  expect(results).toHaveNoViolations();
});
```

### Tools

| Tool | Use Case |
|------|----------|
| axe DevTools | Browser extension |
| WAVE | Visual feedback |
| Lighthouse | Performance + a11y |
| VoiceOver | macOS screen reader |
| NVDA | Windows screen reader |

---

## Quick Fixes

### Missing alt text

```tsx
// ❌ Before
<img src="/photo.jpg" />

// ✅ After
<img src="/photo.jpg" alt="Description of image" />
```

### Missing form labels

```tsx
// ❌ Before
<input placeholder="Email" />

// ✅ After
<label htmlFor="email">Email</label>
<input id="email" placeholder="Email" />
```

### Low contrast text

```css
/* ❌ Before: 2.5:1 ratio */
.text { color: #999; }

/* ✅ After: 4.5:1 ratio */
.text { color: #595959; }
```

### Non-focusable interactive

```tsx
// ❌ Before
<div onClick={handleClick}>Click me</div>

// ✅ After
<button onClick={handleClick}>Click me</button>
```
