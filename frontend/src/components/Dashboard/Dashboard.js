import React, { useEffect, useState } from 'react';
import styles from './Dashboard.module.scss';

const Dashboard = () => {
  const [projects, setProjects] = useState([]);
  const [error, setError] = useState(null);    // State to store error messages
  const [loading, setLoading] = useState(true); // State to handle loading state

  useEffect(() => {
    // Function to fetch projects from the API
    const fetchProjects = async () => {
      try {
        const response = await fetch('/api/projects'); // Make the GET request
        if (!response.ok) {
          throw new Error(`HTTP error! status: ${response.status}`);
        }
        const data = await response.json(); // Parse the response JSON
        console.log("Data", data);
        setProjects(data);                 // Update state with fetched projects
      } catch (error) {
        setError(error.message);           // Handle errors
      } finally {
        setLoading(false);                 // Set loading to false after completion
      }
    };

    fetchProjects();
  }, []); // Empty dependency array ensures this runs only once when the component mounts


  const handleCreateProject = () => {
    const newId = projects.length ? projects[projects.length - 1].id + 1 : 1;
    const newProject = { id: newId, name: `Project ${newId}` };
    setProjects([...projects, newProject]);
  };

  const handleDeleteProject = (projectId) => {
    setProjects(projects.filter((project) => project.id !== projectId));
  };

  if (loading) {
    return <div>Loading...</div>;
  }

  if (error) {
    return <div>Error: {error}</div>;
  }


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
                <span>{project.title}</span>
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
