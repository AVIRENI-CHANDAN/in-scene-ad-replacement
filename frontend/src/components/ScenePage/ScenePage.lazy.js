import React, { lazy, Suspense } from 'react';

const LazyScenePage = lazy(() => import('./ScenePage'));

const ScenePage = props => (
  <Suspense fallback={null}>
    <LazyScenePage {...props} />
  </Suspense>
);

export default ScenePage;
