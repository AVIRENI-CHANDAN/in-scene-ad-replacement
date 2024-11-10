import React, { useState } from 'react';
import styles from './Dashboard.module.scss';

const Dashboard = () => {
  const [projects, setProjects] = useState([
    { id: 1, name: 'Project Alpha' },
    { id: 2, name: 'Project Beta' },
    { id: 3, name: 'Project Gamma' },
    { id: 4, name: 'Project Delta' },
    { id: 5, name: 'Project Epsilon' },
    { id: 6, name: 'Project Alpha' },
    { id: 7, name: 'Project Beta' },
    { id: 8, name: 'Project Gamma' },
    { id: 9, name: 'Project Delta' },
    { id: 10, name: 'Project Epsilon' },
    { id: 11, name: 'Project Alpha' },
    { id: 12, name: 'Project Beta' },
    { id: 13, name: 'Project Gamma' },
    { id: 14, name: 'Project Delta' },
    { id: 15, name: 'Project Epsilon' },
  ]);

  const handleCreateProject = () => {
    const newId = projects.length ? projects[projects.length - 1].id + 1 : 1;
    const newProject = { id: newId, name: `Project ${newId}` };
    setProjects([...projects, newProject]);
  };

  const handleDeleteProject = (projectId) => {
    setProjects(projects.filter((project) => project.id !== projectId));
  };

  return (
    <div className={styles.Dashboard}>
      <div className={styles.TitleGroup}>
        <h1 className={styles.Title}>My Projects Dashboard</h1>
        <div className={styles.ActionButtons}>
          <button onClick={handleCreateProject} className={styles.Button}>
            + Create New Project
          </button>
        </div>
      </div>
      <div className={styles.ProjectsContainer}>
        {projects.length > 0 ? (
          <ul className={styles.ProjectList}>
            {projects.map((project) => (
              <li key={project.id} className={styles.ProjectItem}>
                <span>{project.name}</span>
                <button
                  onClick={() => handleDeleteProject(project.id)}
                  className={styles.DeleteButton}
                >
                  Delete
                </button>
              </li>
            ))}
          </ul>
        ) : (
          <p className={styles.NoProjectsMessage}>No projects available</p>
        )}
      </div>
    </div>
  );
};

export default Dashboard;
