# Framework-Specific Testing Guide

## React Testing

### Component Testing
- Use `@testing-library/react` for component tests
- Test user behavior, not implementation details
- Check for proper `useState`, `useEffect` cleanup
- Verify `useMemo`/`useCallback` usage for performance

### Common React Issues
- Missing keys in lists
- Stale closures in useEffect
- Prop drilling (consider Context)
- Missing dependency arrays
- Unnecessary re-renders

### React DevTools Checks
- Check component tree structure
- Verify props and state values
- Profile component render times

## Vue Testing

### Component Testing
- Use `@vue/test-utils` for component tests
- Test reactive state changes
- Verify computed properties
- Check watcher behavior

### Common Vue Issues
- Missing `v-key` in v-for
- Reactive property declaration issues
- Prop validation missing
- Lifecycle hook timing issues
- Template reactivity caveats

### Vue DevTools Checks
- Inspect component hierarchy
- Monitor Vuex/Pinia state
- Check Vue Router navigation

## General JavaScript Testing

### Vanilla JS Checks
- Event listeners properly removed
- No global namespace pollution
- Proper event delegation
- Memory leak prevention

### DOM Manipulation
- Batch DOM reads/writes
- Document fragments for multiple insertions
- Proper cleanup of timers/intervals
