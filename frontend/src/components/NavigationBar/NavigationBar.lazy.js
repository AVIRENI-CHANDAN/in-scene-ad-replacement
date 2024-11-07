import React, { lazy, Suspense } from 'react';

const LazyNavigationBar = lazy(() => import('./NavigationBar'));

const NavigationBar = props => (
  <Suspense fallback={null}>
    <LazyNavigationBar {...props} />
  </Suspense>
);

export default NavigationBar;
