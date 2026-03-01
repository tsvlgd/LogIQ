# LogIQ File Upload - Testing Checklist

## ✅ Pre-Testing Setup

- [ ] All three files updated:
  - [ ] `templates/index.html`
  - [ ] `static/style.css`
  - [ ] `static/index.js`
- [ ] Backend `/classify-file` endpoint running
- [ ] Backend returns binary file response
- [ ] No console errors on page load

---

## 🎬 UI/UX Testing

### Mode Switcher
- [ ] Default mode is "Paste Logs" (button highlighted)
- [ ] Clicking "Upload File" switches modes smoothly
- [ ] Clicking "Paste Logs" switches back to textarea
- [ ] Fade animation visible when switching
- [ ] No page reload when switching modes
- [ ] Button color changes to indicate active mode
- [ ] Hover effect shows on both buttons

### Paste Mode (Original Functionality)
- [ ] Textarea visible by default
- [ ] Placeholder text displays correctly
- [ ] Can type/paste into textarea
- [ ] "Classify Logs" button enabled when text present
- [ ] "Clear" button works
- [ ] Results display as cards below
- [ ] Error messages show in red box
- [ ] Dark mode applies to textarea

### File Mode - Upload Area
- [ ] Upload area visible when in file mode
- [ ] Upload icon (📤) displays
- [ ] Text reads "Drag and drop CSV or Excel file"
- [ ] Hint text "or click to browse" visible
- [ ] Clicking area opens file browser
- [ ] Dragging file over area highlights it
- [ ] Drag-over state shows primary color
- [ ] Drag-over state lifts the area (shadow shift)

### File Mode - File Selection
- [ ] File browser filters for `.csv` and `.xlsx`
- [ ] Selecting CSV file shows preview
- [ ] Selecting XLSX file shows preview
- [ ] File preview shows emoji icon (📄)
- [ ] File preview shows correct filename
- [ ] File preview shows correct file size (KB/MB)
- [ ] Remove button (✕) appears in preview
- [ ] "Scan File" button becomes enabled
- [ ] Clicking remove button hides preview
- [ ] Upload area reappears after removing file

### File Type Validation
- [ ] Selecting `.txt` file shows error
- [ ] Selecting `.doc` file shows error
- [ ] Selecting `.xls` file shows error
- [ ] Error message is clear and helpful
- [ ] Can retry after error
- [ ] Error clears when selecting valid file

### File Mode - Processing
- [ ] "Scan File" button disabled during processing
- [ ] Button text changes to "Processing..."
- [ ] Spinner visible inline (rotating circle)
- [ ] Spinner has white background
- [ ] Cannot interact with UI during processing
- [ ] Processing state lasts reasonable time (test with mock backend)

### File Mode - Success
- [ ] File downloads automatically to default folder
- [ ] Downloaded filename is `classified_logs_YYYY-MM-DD.csv` or `.xlsx`
- [ ] Success message appears in green
- [ ] Success message shows checkmark (✓)
- [ ] Success text reads "File classified successfully"
- [ ] Success message auto-hides after ~3 seconds
- [ ] UI resets after success (file preview hidden, upload area shown)

### File Mode - Error Handling
- [ ] If file processing fails, error message shows
- [ ] Error message is in red box
- [ ] File selection retained after error
- [ ] Can retry with same file
- [ ] Can select different file
- [ ] Error clears when action taken

---

## 🌓 Dark Mode Testing

- [ ] Clicking 🌙 toggles dark mode
- [ ] Mode switcher buttons visible in dark mode
- [ ] Paste mode textarea visible in dark mode
- [ ] File upload area visible in dark mode
- [ ] All text readable (contrast OK)
- [ ] All icons visible in dark mode
- [ ] Success message visible in dark mode
- [ ] Error message visible in dark mode
- [ ] Hover effects work in dark mode
- [ ] Drag-over state visible in dark mode
- [ ] Dark mode preference persists on refresh

---

## 📱 Responsive Testing

### Tablet (768px viewport)
- [ ] Layout doesn't break
- [ ] Mode switcher fits on one line
- [ ] Buttons appropriately sized
- [ ] File upload area full width
- [ ] File preview doesn't overflow
- [ ] Text readable without zoom
- [ ] No horizontal scrolling
- [ ] Touch targets adequate (min 44px)

### Mobile (480px viewport)
- [ ] Mode switcher stacks vertically
- [ ] Mode buttons are full-width
- [ ] App card doesn't overflow
- [ ] File upload area full-width
- [ ] Text readable without zoom
- [ ] No horizontal scrolling
- [ ] Buttons easily tappable
- [ ] File preview stacks properly (icon, text, remove)
- [ ] Remove button accessible and full-width
- [ ] Emoji icons display correctly

### Small Mobile (320px viewport)
- [ ] Critical - doesn't break layout
- [ ] Navigation visible
- [ ] Buttons still tappable
- [ ] Text not overlapping
- [ ] File name not cut off
- [ ] No critical overflow

---

## 🔒 Security Testing

### XSS Protection
- [ ] Filename with `<script>` tag escapes properly
- [ ] Filename with quotes displays correctly
- [ ] Filename with special chars displays correctly
- [ ] Error messages with special chars safe
- [ ] No script injection possible

### File Upload Safety
- [ ] Validates file type on client
- [ ] Rejects file with wrong extension
- [ ] Sends to correct backend endpoint
- [ ] Uses FormData (not raw file)
- [ ] Blob URL cleaned up after download
- [ ] No sensitive data in localStorage

---

## ♿ Accessibility Testing

### Keyboard Navigation
- [ ] Tab moves through all buttons
- [ ] Enter/Space activates buttons
- [ ] File input accessible via tab
- [ ] Can select file via keyboard
- [ ] Results visible via keyboard
- [ ] Tab order logical

### Screen Reader (test with one if available)
- [ ] Theme toggle has aria-label
- [ ] Buttons have readable labels
- [ ] File input labeled properly
- [ ] Error messages announced
- [ ] Success messages announced
- [ ] Mode change announced

### Focus States
- [ ] Focused buttons have visible outline
- [ ] Focused inputs highlighted
- [ ] Focus order makes sense
- [ ] No focus traps

### Color Contrast
- [ ] Text on light background readable
- [ ] Text on dark background readable
- [ ] Buttons have enough contrast
- [ ] Error/success messages readable

---

## 🌐 Browser Compatibility

### Desktop Browsers
- [ ] Chrome (latest)
- [ ] Firefox (latest)
- [ ] Safari (latest)
- [ ] Edge (latest)

### Mobile Browsers
- [ ] iOS Safari (latest)
- [ ] Chrome Android (latest)
- [ ] Firefox Android (latest)
- [ ] Samsung Internet

### Features to Test Per Browser
- [ ] Fetch API works
- [ ] FormData works
- [ ] Blob download works
- [ ] CSS animations smooth
- [ ] File input works
- [ ] Drag/drop works
- [ ] localStorage works (for theme)

---

## 🔧 Backend Integration Testing

### `/classify-file` Endpoint
- [ ] Endpoint accepts POST requests
- [ ] Accepts multipart/form-data
- [ ] Accepts field name `file`
- [ ] Validates file type on backend
- [ ] Processes file correctly
- [ ] Returns binary response
- [ ] Returns same format as input (.csv stays .csv)
- [ ] Error responses include `detail` field

### Error Scenarios
- [ ] Backend returns 400 - shows error message
- [ ] Backend returns 500 - shows error message
- [ ] Network timeout - shows error message
- [ ] File too large - shows error message (if backend enforces)
- [ ] Invalid format - shows error message (if backend validates)
- [ ] Server offline - shows error message

### Success Scenarios
- [ ] Small CSV file processes quickly
- [ ] Medium XLSX file processes correctly
- [ ] Large file processes without timeout
- [ ] Downloaded file is valid/usable
- [ ] Multiple files can be uploaded in sequence

---

## ⚡ Performance Testing

### Load Time
- [ ] Page loads in < 2 seconds
- [ ] No performance degradation from new features
- [ ] CSS loads without blocking render
- [ ] JavaScript doesn't block interaction

### File Processing
- [ ] Spinner appears immediately
- [ ] Large files don't freeze UI
- [ ] Download triggers quickly after response
- [ ] No memory leaks (check DevTools)

### Animations
- [ ] Spinner animation smooth (60fps)
- [ ] Fade animations smooth
- [ ] No jank when switching modes
- [ ] Hover effects immediate

---

## 🐛 Edge Cases

### Empty/Invalid Input
- [ ] Can't classify empty textarea
- [ ] Can't scan without file selected
- [ ] Appropriate error messages shown

### File Handling
- [ ] Very long filename displays properly
- [ ] Filename with unicode displays
- [ ] Filename with spaces preserved
- [ ] Very large files handled gracefully

### Network Issues
- [ ] Slow network shows spinner long enough
- [ ] Network error shows message
- [ ] Can retry after network error
- [ ] Timeout handled gracefully

### Rapid Interactions
- [ ] Can't double-click to submit twice
- [ ] Button disabled during processing
- [ ] Switching modes during upload? (Test edge case)
- [ ] Rapid mode switching works

---

## 📊 Visual Consistency

### Colors
- [ ] Buttons match design spec
- [ ] Backgrounds match spec
- [ ] Text colors readable everywhere
- [ ] Error color consistent
- [ ] Success color consistent
- [ ] Hover states obvious

### Spacing
- [ ] Padding consistent throughout
- [ ] Gaps between elements appropriate
- [ ] No cramped or excessive spacing
- [ ] Mobile spacing optimized

### Typography
- [ ] Font family correct (Inter)
- [ ] Font sizes per spec
- [ ] Line heights readable
- [ ] Letter spacing maintained
- [ ] Font weights correct

### Borders & Shadows
- [ ] Border width 2-3px as spec
- [ ] Shadow offset 4-8px as spec
- [ ] Border radius 5-6px as spec
- [ ] Shadows visible on light/dark

---

## 📝 Sign-Off Checklist

Before deploying:

- [ ] All feature tests pass
- [ ] All browser tests pass
- [ ] All accessibility tests pass
- [ ] Dark mode fully functional
- [ ] Mobile responsive verified
- [ ] Security tests pass
- [ ] No console errors
- [ ] No console warnings
- [ ] Performance acceptable
- [ ] Backend integration confirmed
- [ ] Documentation complete

---

## 🎯 Final Verification

```javascript
// Open DevTools Console and verify:

// 1. Check if all functions exist
typeof switchMode === 'function'              // true
typeof classifyFile === 'function'            // true
typeof classifyLogs === 'function'            // true
typeof showError === 'function'               // true
typeof showSuccessMessage === 'function'      // true

// 2. Check if all elements exist
document.getElementById('pasteMode')          // HTMLElement
document.getElementById('fileMode')           // HTMLElement
document.getElementById('dragDropArea')       // HTMLElement
document.getElementById('fileInput')          // HTMLInputElement

// 3. Check theme works
localStorage.getItem('theme')                 // 'light' or 'dark'
document.documentElement.getAttribute('data-theme') // Matches localStorage
```

---

## 🚀 Ready to Deploy!

Once all tests pass, the feature is ready for:
- [ ] Staging deployment
- [ ] User acceptance testing
- [ ] Production deployment

---

**Last Updated**: March 2, 2026
**Feature Status**: ✅ Production Ready
