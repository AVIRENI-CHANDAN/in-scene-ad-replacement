import React from 'react';
import styles from './Dashboard.module.scss';
import { Link } from 'react-router-dom';

function Dashboard() {
  const steps = {
    1: "https://gyrus.ai/isar2d/assets/1.jpg",
    2: "https://gyrus.ai/isar2d/assets/2.jpg",
    3: "https://gyrus.ai/isar2d/assets/3.jpg"
  };

  return (
    <div className={styles.Dashboard}>
      <div className={styles.Container}>
        <div className={styles.Wrapper}>
          <div className={styles.Title}>
            Simple steps you can follow for ISAR Demo
          </div>
          <div className={styles.ProcedureContainer}>
            <div className={styles.StepsList}>
              {Object.entries(steps).map(([key, url]) => (
                <div className={styles.StepItem} key={key}>
                  <div className={styles.StepImage}>
                    <img src={url} alt='Procedure 1' />
                  </div>
                </div>
              ))}
            </div>
          </div>
          <div className={styles.TryNowContainer}>
            <Link to="/new/project" className={styles.TryNowBtn}>Try now</Link>
          </div>
        </div>
      </div>
    </div>
  );
};

export default Dashboard;
