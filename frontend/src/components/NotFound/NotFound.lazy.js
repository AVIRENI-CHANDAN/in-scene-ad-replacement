import React, { lazy, Suspense } from 'react';

const LazyNotFound = lazy(() => import('./NotFound'));

const NotFound = props => (
  <Suspense fallback={null}>
    <LazyNotFound {...props} />
  </Suspense>
);

export default NotFound;
