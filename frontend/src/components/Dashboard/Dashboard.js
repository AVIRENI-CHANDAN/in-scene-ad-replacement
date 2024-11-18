import React, { useEffect, useState } from 'react';
import { useNavigate } from 'react-router-dom';
import styles from './Dashboard.module.scss';

const Dashboard = () => {
  const [projects, setProjects] = useState([]);
  const [error, setError] = useState(null);    // State to store error messages
  const [loading, setLoading] = useState(true); // State to handle loading state
  const [fetch_data, setFetchData] = useState(true);
  const navigate = useNavigate();

  useEffect(() => {
    // Function to fetch projects from the API
    const fetchProjects = async () => {
      if (fetch_data) {
        try {
          const response = await fetch('/api/projects', {
            method: 'GET',
            credentials: 'include'
          }); // Make the GET request
          if (!response.ok) {
            const errorMessages = {
              400: 'Invalid request. Please try again.',
              401: 'Please log in to continue.',
              403: 'You don\'t have permission to access this resource.',
              404: 'Project data not found.',
              500: 'Server error. Please try again later.'
            };
            throw new Error(errorMessages[response.status] || `Server error ${response.status}`);
          }
          const data = await response.json(); // Parse the response JSON
          console.log("Data", data);
          setProjects(data);                 // Update state with fetched projects
        } catch (error) {
          setError(error.message);           // Handle errors
        } finally {
          setLoading(false);                 // Set loading to false after completion
          setFetchData(false);
        }
      }
    };

    fetchProjects();
  }, [fetch_data]); // Empty dependency array ensures this runs only once when the component mounts


  const handleCreateProject = () => {
    navigate("/new/project");
  };

  const handleDeleteProject = async (projectId) => {
    setLoading(true);
    try {
      const response = await fetch(`api/projects/${projectId}/delete`, {
        method: 'POST',
        credentials: 'include'
      });
      if (!response.ok) {
        const errorMessages = {
          400: 'Invalid request. Please try again.',
          401: 'Please log in to continue.',
          403: 'You don\'t have permission to access this resource.',
          404: 'Project data not found.',
          500: 'Server error. Please try again later.'
        };
        throw new Error(errorMessages[response.status] || `Server error ${response.status}`);
      }
      const data = await response.json();
      console.log("Data", data);
      setProjects([]);
      setFetchData(true);
    }
    catch (error) {
      setError(error.message);
    } finally {
      setLoading(false);
    }
  };

  if (loading || fetch_data) {
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
