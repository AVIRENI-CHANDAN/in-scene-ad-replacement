import React from 'react';
import styles from './ScenePage.module.scss';
import { useParams } from 'react-router-dom';

function ScenePage() {
  const { project_id } = useParams();
  console.log("Project id", project_id);
  return (
    <div className={styles.ScenePage}>
      ScenePage Component - {project_id}
    </div>
  );
}

ScenePage.propTypes = {};

ScenePage.defaultProps = {};

export default ScenePage;
