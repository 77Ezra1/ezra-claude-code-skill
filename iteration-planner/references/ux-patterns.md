# UX Patterns

Common UX improvements and interaction patterns.

## Loading States

### What to Look For
- Forms without loading indication
- Buttons that don't show action progress
- Pages with blank states during fetch
- No feedback for long-running operations

### Quick Wins
```tsx
// Before: No loading state
<button onClick={handleSubmit}>Submit</button>

// After: With loading state
<button onClick={handleSubmit} disabled={isLoading}>
  {isLoading ? <Spinner /> : 'Submit'}
</button>
```

## Empty States

### Common Empty States Needed

| State | Message Suggestion | Action |
|-------|-------------------|--------|
| No documents | "You haven't uploaded any documents yet" | Upload button |
| No search results | "No results found for '{query}'" | Clear search |
| No notifications | "You're all caught up!" | - |
| Error state | "Something went wrong" | Retry button |
| No team members | "Invite team members to collaborate" | Invite button |

## Form UX

### Validation Timing
| Validation Type | When to Show |
|----------------|--------------|
| Required fields | On blur (when leaving field) |
| Format (email, phone) | On blur |
| Password strength | As user types |
| Async (username taken) | Debounced, after user stops typing |

### Error Messages
```tsx
// Bad: Generic error
"Invalid input"

// Good: Specific, actionable
"Password must be at least 8 characters"
"Username is already taken, try another"
"Email address format is incorrect"
```

## Feedback & Notifications

### Action Feedback

| Action | Feedback |
|--------|----------|
| Delete | "Deleted successfully" + undo option |
| Copy | "Copied to clipboard" toast |
| Save | Auto-save indicator or "Saved" |
| Send | "Message sent" |
| Export | Download starts or "Preparing export..." |
| Share | "Link copied to clipboard" |

## Navigation

### Breadcrumbs
Needed when:
- Depth > 2 levels
- Multiple paths to same content
- Hierarchical content (folders, categories)

### Pagination vs Infinite Scroll

| Use Pagination When | Use Infinite Scroll When |
|---------------------|--------------------------|
| Need to reach end of results | Social feed style content |
| Need to preserve position | Discovery/exploration |
| Results can be bookmarked | Content updates frequently |
| Mobile experience matters | Desktop-first experience |

## Search UX

### Search Input Improvements

| Feature | Description | Priority |
|---------|-------------|----------|
| Keyboard shortcut | Cmd/Ctrl + K to focus | P1 |
| Clear button | × to clear input | P1 |
| Search as you type | Debounced search | P1 |
| Recent searches | Quick access to history | P2 |
| Filters | Refine search results | P1 |
| Result highlighting | Bold matching terms | P2 |

## Mobile Responsiveness

### Common Issues

| Issue | Solution |
|-------|----------|
| Tables overflow | Horizontal scroll or card view |
| Modals too tall | Scrollable content, fixed header |
| Hover states missing | Add active/active states |
| Tap targets too small | Min 44×44px |
| Text too small | Min 16px for body |

## Accessibility Quick Wins

| Issue | Fix |
|-------|-----|
| Missing alt text | Add descriptive alt to images |
| No aria labels | Add aria-label to icon buttons |
| Keyboard trap | Ensure Esc closes modals |
| No focus visible | Add :focus-visible styles |
| Low contrast | Increase color contrast ratio |

## Performance Perception

Even if actual performance is good, perception matters:

| Technique | Effect |
|-----------|--------|
| Skeleton screens | Faster perceived load |
| Optimistic updates | Instant feel, revert on error |
| Progressive image load | Show blurry → sharp |
| Stagger animations | Content feels organized |
| Prefetch | Navigation feels instant |

## Dark Mode

### Implementation Checklist
- [ ] CSS variables for colors
- [ ] System preference detection
- [ ] User preference persisted
- [ ] Images/graphs adapt to theme
- [ ] Good contrast in both modes
- [ ] Smooth transition between modes

## Onboarding

### First Run Experience

| Pattern | When to Use |
|---------|-------------|
| Product tour | Complex product with many features |
| Interactive tutorial | Action-based product |
| Empty state with CTA | Simple, focused product |
| Progressive disclosure | Feature-rich product |
| Video walkthrough | Visual product |

## Error Boundaries

### Graceful Degradation

| Error Type | User-Facing Message |
|------------|---------------------|
| Network error | "Unable to connect. Check your internet." |
| Server error | "Something went wrong. Please try again." |
| Not found | "This page doesn't exist or was removed." |
| Permission denied | "You don't have access to this resource." |
| Rate limit | "Too many requests. Please wait a moment." |
