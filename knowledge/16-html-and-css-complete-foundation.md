# HTML and CSS — Complete Web Interface Foundation

- **Document ID:** KB-WEB-HTML-CSS-16
- **Status:** general technical guidance
- **Applies to:** browser interfaces, React applications, accessibility and responsive design
- **Keywords:** HTML, CSS, semantic HTML, DOM, Flexbox, Grid, responsive design, box model, selector, cascade, accessibility, layout bug, verkkosivu, tyylit, responsiivisuus

## 1. Roles of HTML, CSS and JavaScript

- **HTML** describes content and its semantic structure.
- **CSS** controls presentation, layout, typography, colors and responsive behavior.
- **JavaScript** adds behavior and interaction.
- **React** uses JavaScript/TypeScript to compose UI from components; it still renders HTML elements styled with CSS.

Keep content, presentation and behavior conceptually separate.

## 2. Minimal HTML document

```html
<!doctype html>
<html lang="en">
<head>
  <meta charset="utf-8">
  <meta name="viewport" content="width=device-width, initial-scale=1">
  <title>Example page</title>
  <link rel="stylesheet" href="styles.css">
</head>
<body>
  <header><h1>Welcome</h1></header>
  <main>
    <p>A semantic HTML page.</p>
    <a href="/help">Get help</a>
  </main>
</body>
</html>
```

Use the correct document type, character encoding, viewport and page language. Use headings in a logical hierarchy.

## 3. Important semantic elements

- Page regions: `header`, `nav`, `main`, `section`, `article`, `aside`, `footer`.
- Text: `h1`–`h6`, `p`, `strong`, `em`, `blockquote`.
- Links and actions: `a` navigates; `button` performs an action.
- Lists: `ul`, `ol`, `li`.
- Forms: `form`, `label`, `input`, `select`, `textarea`, `button`.
- Tables: `table`, `caption`, `thead`, `tbody`, `th`, `td`.

Choose elements by meaning, not by their default appearance. Associate every form control with a visible label. Use alt text for informative images and empty alt text for decorative images.

## 4. CSS basics

```css
.card {
  max-width: 42rem;
  margin: 1rem auto;
  padding: 1rem;
  border: 1px solid #ccc;
  border-radius: 0.5rem;
}

.card h2 {
  margin-top: 0;
}
```

A CSS rule has a selector and declarations. The cascade considers origin, importance, specificity and source order. Prefer simple selectors and avoid escalating specificity to fight earlier rules.

## 5. Box model

By default, an element's declared width applies to its content box; padding and border add to its outer size. A common baseline is:

```css
*, *::before, *::after {
  box-sizing: border-box;
}
```

Understand content, padding, border and margin when diagnosing unexpected dimensions.

## 6. Layout: Flexbox and Grid

- Use **Flexbox** for arranging items primarily along one axis, such as a toolbar or navigation row.
- Use **CSS Grid** for two-dimensional layouts, such as a page shell or card grid.
- Avoid using floats for modern application layout.
- Avoid fixed widths that cause overflow on small screens.

```css
.toolbar {
  display: flex;
  align-items: center;
  justify-content: space-between;
  gap: 1rem;
  flex-wrap: wrap;
}

.card-grid {
  display: grid;
  grid-template-columns: repeat(auto-fit, minmax(min(100%, 16rem), 1fr));
  gap: 1rem;
}
```

## 7. Responsive design

Start with a usable narrow layout, then add breakpoints when the content needs them. Prefer flexible units, max-widths and responsive images.

```css
img {
  max-width: 100%;
  height: auto;
}

@media (min-width: 48rem) {
  .page {
    padding: 2rem;
  }
}
```

Test with browser dev tools at multiple widths and zoom levels. Do not rely on one specific phone or monitor size.

## 8. Accessibility essentials

- Use semantic HTML and a logical heading order.
- Ensure keyboard access and visible focus indicators.
- Provide labels and useful error messages for forms.
- Maintain sufficient text/background contrast.
- Do not communicate state by color alone.
- Give buttons clear accessible names.
- Respect reduced-motion preferences.
- Test keyboard-only navigation and screen-reader semantics.

## 9. Common HTML/CSS problems

- **CSS not loading:** verify file path, filename case, network request and cache.
- **Style appears overridden:** inspect computed styles, specificity, cascade layers and media queries.
- **Unexpected horizontal scrollbar:** inspect fixed widths, long unbroken text, margins and overflowing children.
- **Flex item refuses to shrink:** check `min-width: auto`; `min-width: 0` may be appropriate.
- **Grid columns too wide:** use flexible tracks such as `minmax(0, 1fr)`.
- **Element behind another:** inspect stacking contexts, positioning and z-index; a large z-index cannot escape every stacking context.
- **Image distorted:** use `width`, `height`, `object-fit` and intrinsic aspect ratio intentionally.
- **Margin collapse surprises:** inspect parent/child block margins and layout context.
- **Page differs across browsers:** use standards-based CSS, test target browsers and avoid unsupported experimental properties.

## 10. HTML/CSS in AI HelpDesk

The frontend is React + TypeScript. Component structure belongs in React/TSX, while CSS defines visual styling. When modifying UI, preserve semantic controls, keyboard behavior, responsive layout and the project's existing styling conventions. Do not introduce raw HTML rendering for untrusted AI output.


## Tiivistelmä suomeksi

HTML määrittelee verkkosivun rakenteen ja merkityksen, CSS ulkoasun ja asettelun sekä JavaScript toiminnallisuuden. Käytä semanttisia HTML-elementtejä, jotta sisältö on ymmärrettävä myös apuvälineille. CSS:n Box Model, cascade, specificity, Flexbox ja Grid selittävät suuren osan asetteluongelmista. Responsiivinen suunnittelu mukauttaa näkymän eri näyttöleveyksille. Saavutettavuus, kontrasti, näppäimistökäyttö ja lomakekenttien nimet kuuluvat hyvään toteutukseen.
