import React from 'react';
import { useNavigate } from 'react-router-dom';
import styles from './NewProject.module.scss';

function NewProject() {
  const [projectTitle, setProjectTitle] = React.useState('');
  const [projectDescription, setProjectDescription] = React.useState('');
  const [error, setError] = React.useState('');
  const navigate = useNavigate();

  const formSubmit = (event) => {
    event.preventDefault();
    console.log("Form submit");
    fetch("/api/projects", {
      method: "POST",
      headers: {
        "Content-Type": "application/json",
      },
      body: JSON.stringify({
        title: projectTitle,
        description: projectDescription,
      }),

    }).then((response) => {
      if (response.ok) {
        setProjectDescription('');
        setProjectTitle('');
        navigate("/dashboard");
      }
      return response.json().then((data) => {
        console.log("Data", data);
        setError(data.error || "An unknown error occurred.");
      });
    }).catch((error) => {
      setError("A network error occurred. Please try again later.");
    });
  };

  useEffect(() => {
    if (error) {
      const timer = setTimeout(() => {
        setError('');
      }, 3000);
      return () => clearTimeout(timer);
    }
  }, [error]);

  const handleTitleChange = (event) => { setProjectTitle(event.target.value); };
  const handleDescriptionChange = (event) => { setProjectDescription(event.target.value); };

  return (
    <div className={styles.NewProject}>
      <div className={styles.Container}>
        <div className={styles.Wrapper}>
          <div className={styles.Header}>New Project</div>
          <div className={styles.FormContainer}>
            <div className={styles.FormWrapper}>
              <div className={styles.FormError}>{error}</div>
              <form className={styles.Form} onSubmit={formSubmit}>
                <div className={styles.FormGroup}>
                  <input className={styles.FormField} type='text' placeholder='Project Name' autoComplete='off' autoFocus value={projectTitle} onChange={handleTitleChange} />
                </div>
                <div className={styles.FormGroup}>
                  <input className={styles.FormField} type='text' placeholder='Project Description' autoComplete='off' value={projectDescription} onChange={handleDescriptionChange} />
                </div>
                <div className={styles.FormGroup}>
                  <button className={styles.FormButton} type='submit'>Create Project</button>
                </div>
              </form>
            </div>
          </div>
        </div>
      </div>
    </div>
  );
}

NewProject.propTypes = {};

NewProject.defaultProps = {};

export default NewProject;
