import React, { useEffect, useState } from 'react';
import { useNavigate } from 'react-router-dom';
import styles from './NewProject.module.scss';

function NewProject() {
  const [projectTitle, setProjectTitle] = useState('');
  const [projectDescription, setProjectDescription] = useState('');
  const [error, setError] = useState('');
  const [isSubmitting, setIsSubmitting] = useState(false);
  const [user, setUser] = useState('Anonymous User');
  const [file, setFile] = useState(null);

  const navigate = useNavigate();

  const formSubmit = async (event) => {
    setIsSubmitting(true);
    event.preventDefault();
    if (!projectTitle.trim() || !projectDescription.trim()) {
      setError("Project title and description are required");
      setIsSubmitting(false);
      return;
    }

    if (file) {
      console.log("File", file);
    }

    const formData = new FormData();
    formData.append("title", projectTitle);
    formData.append("description", projectDescription);
    formData.append("file", file);

    setError('');
    console.log("Form submit");
    await fetch("/api/projects", {
      method: "POST",
      credentials: 'include',
      body: formData
    }).then((response) => {
      console.log("The response", response);
      if (response.ok) {
        response.json().then(data => {
          setProjectTitle('');
          setProjectDescription('');
          setFile(null);
          navigate(`/project/${data.project_id}`);
        });
      } else {
        response.json().then(data => setError(data.error));
        setIsSubmitting(false);
      }
    }).catch((error) => {
      setError("A network error occurred. Please try again later.");
      setIsSubmitting(false);
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
  const handleFileChange = (e) => {
    console.log("Event target", e.target.files);
    if (e.target.files && e.target.files[0]) {
      setFile(e.target.files[0]);
    }
  };

  return (
    <div className={styles.NewProject}>
      <div className={styles.Container}>
        <div className={styles.Greeting}>
          <div className={styles.Message}>
            Welcome
          </div>
          <div className={styles.Username}>
            {user}
          </div>
        </div>
        <div className={styles.NewProjectContainer}>
          <div className={styles.NewProjectWrapper}>
            <div className={styles.IntroBox}>
              <div className={styles.IntroWrapper}>
                <div className={styles.HeadingImage}>
                  <img src="https://gyrus.ai/assets/videodemoassets/videoeditor/video.png" alt="heading-image" />
                </div>
                <div className={styles.HeadingCaption}>
                  Create a project to explore logo placement model
                </div>
              </div>
              <div className={styles.InstructionsWrapper}>
                <div className={styles.InstructionBox}>
                  <ol className={styles.InstructionList}>
                    <li className={styles.ListItem}>Create a project if not created</li>
                    <li className={styles.ListItem}>Give proper name for your project</li>
                    <li className={styles.ListItem}>Choose a video for logo placement and then proceed with further steps</li>
                    <li className={styles.ListItem}>Delete the project in-case if you want to start with new video or project</li>
                  </ol>
                </div>
              </div>
            </div>
            <div className={styles.NewFormBox}>
              <div className={styles.NewFormContainer}>
                <div className={styles.NewFormWrapper}>
                  <form className={styles.Form} onSubmit={formSubmit}>
                    <div className={styles.FormGroup}>
                      <input className={styles.FormField} type='text' placeholder='Project Name' autoComplete='off' autoFocus value={projectTitle} onChange={handleTitleChange} />
                    </div>
                    <div className={styles.FormGroup}>
                      <textarea className={styles.FormField} type='text' placeholder='Project Description' autoComplete='off' value={projectDescription} onChange={handleDescriptionChange} cols={1} rows={3} />
                    </div>
                    <div className={styles.FormGroup}>
                      <label className={styles.FileLabel} htmlFor='input-file'>
                        <span className={styles.FileLabelBtn}>Browse..</span>
                        <span className={styles.FileName}>{file ? file.name : "No file selected."}</span>
                      </label>
                      <input className={styles.FileField} type='file' id='input-file' onChange={handleFileChange} accept='video/*' />
                    </div>
                    <div className={styles.FormGroup}>
                      <button
                        className={styles.FormButton}
                        type='submit'
                        disabled={isSubmitting}
                      >
                        {isSubmitting ? 'Creating...' : 'Create Project'}
                      </button>
                    </div>
                  </form>
                </div>
              </div>
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
