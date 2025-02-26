import React, { useState } from 'react';
import { useNavigate } from 'react-router-dom';
import { ToastContainer, toast } from 'react-toastify';
import 'react-toastify/dist/ReactToastify.css';

const Job = () => {
  const navigate = useNavigate();
  const [formData, setFormData] = useState({
    name: '',
    age: '',
    experience: '',
    education: '',
    skills: '',
    certifications: '',
    preferredJobTitles: '',
    industries: '',
    locations: '',
    salaryExpectations: '',
    languages: '',
    linkedIn: '',
    summary: '',
  });

  const handleChange = (e) => {
    const { name, value } = e.target;
    setFormData((prev) => ({
      ...prev,
      [name]: value,
    }));
  };

  const handleSubmit = async (e) => {
    e.preventDefault();
    // Notify user that the job details are being fetched
    toast.info('Fetching job recommendations...', { autoClose: 2000 });

    // Create an XMLHttpRequest to call the RapidAPI endpoint
    const data = null;
    const xhr = new XMLHttpRequest();
    xhr.withCredentials = true;

    xhr.addEventListener('readystatechange', function () {
      if (this.readyState === this.DONE) {
        try {
          // Parse the JSON response
          const jobDetail = JSON.parse(this.responseText);
          console.log('Job detail:', jobDetail);
          // Navigate to the job-list page, passing the job detail as an array
          navigate('/job-list', { state: { generatedQuery: 'Job Recommendations', jobResults: [jobDetail] } });
        } catch (error) {
          console.error('Error parsing job details:', error);
          toast.error('Error fetching job details. Please try again.');
        }
      }
    });

    xhr.open('GET', 'https://linkedin-data-api.p.rapidapi.com/get-job-details?id=4090994054');
    xhr.setRequestHeader('x-rapidapi-key', '1a6e658d12mshefdf9c6774b3a50p1cf27fjsncf14f79c8cfd');
    xhr.setRequestHeader('x-rapidapi-host', 'linkedin-data-api.p.rapidapi.com');

    xhr.send(data);
  };

  return (
    <div className="min-h-screen flex items-center justify-center bg-gray-100 dark:bg-gray-900 p-4">
      <ToastContainer />
      <div className="w-full max-w-3xl bg-white dark:bg-gray-800 shadow-lg rounded-lg p-8">
        <h2 className="text-3xl font-bold mb-6 text-gray-800 dark:text-gray-100">
          Complete Your Job Profile
        </h2>
        <form onSubmit={handleSubmit} className="space-y-6">
          {/* Basic Info */}
          <div className="grid grid-cols-1 md:grid-cols-2 gap-6">
            <div>
              <label htmlFor="name" className="block text-gray-700 dark:text-gray-300">
                Full Name
              </label>
              <input
                type="text"
                id="name"
                name="name"
                value={formData.name}
                onChange={handleChange}
                required
                className="mt-1 block w-full px-4 py-2 border rounded-md dark:bg-gray-700 dark:text-gray-200"
              />
            </div>
            <div>
              <label htmlFor="age" className="block text-gray-700 dark:text-gray-300">
                Age
              </label>
              <input
                type="number"
                id="age"
                name="age"
                value={formData.age}
                onChange={handleChange}
                required
                className="mt-1 block w-full px-4 py-2 border rounded-md dark:bg-gray-700 dark:text-gray-200"
              />
            </div>
          </div>
          <div className="grid grid-cols-1 md:grid-cols-2 gap-6">
            <div>
              <label htmlFor="experience" className="block text-gray-700 dark:text-gray-300">
                Years of Experience
              </label>
              <input
                type="number"
                id="experience"
                name="experience"
                value={formData.experience}
                onChange={handleChange}
                required
                className="mt-1 block w-full px-4 py-2 border rounded-md dark:bg-gray-700 dark:text-gray-200"
              />
            </div>
            <div>
              <label htmlFor="education" className="block text-gray-700 dark:text-gray-300">
                Highest Education
              </label>
              <input
                type="text"
                id="education"
                name="education"
                value={formData.education}
                onChange={handleChange}
                required
                placeholder="e.g. B.Tech, MSc, etc."
                className="mt-1 block w-full px-4 py-2 border rounded-md dark:bg-gray-700 dark:text-gray-200"
              />
            </div>
          </div>

          {/* Additional Details */}
          <div>
            <label htmlFor="skills" className="block text-gray-700 dark:text-gray-300">
              Skills
            </label>
            <input
              type="text"
              id="skills"
              name="skills"
              value={formData.skills}
              onChange={handleChange}
              placeholder="e.g. JavaScript, Python, React"
              className="mt-1 block w-full px-4 py-2 border rounded-md dark:bg-gray-700 dark:text-gray-200"
            />
          </div>
          <div>
            <label htmlFor="certifications" className="block text-gray-700 dark:text-gray-300">
              Certifications
            </label>
            <input
              type="text"
              id="certifications"
              name="certifications"
              value={formData.certifications}
              onChange={handleChange}
              placeholder="e.g. AWS, PMP"
              className="mt-1 block w-full px-4 py-2 border rounded-md dark:bg-gray-700 dark:text-gray-200"
            />
          </div>
          <div>
            <label htmlFor="preferredJobTitles" className="block text-gray-700 dark:text-gray-300">
              Preferred Job Titles
            </label>
            <input
              type="text"
              id="preferredJobTitles"
              name="preferredJobTitles"
              value={formData.preferredJobTitles}
              onChange={handleChange}
              placeholder="e.g. Software Engineer, Data Analyst"
              className="mt-1 block w-full px-4 py-2 border rounded-md dark:bg-gray-700 dark:text-gray-200"
            />
          </div>
          <div>
            <label htmlFor="industries" className="block text-gray-700 dark:text-gray-300">
              Industry Interests
            </label>
            <input
              type="text"
              id="industries"
              name="industries"
              value={formData.industries}
              onChange={handleChange}
              placeholder="e.g. Finance, Healthcare, Tech"
              className="mt-1 block w-full px-4 py-2 border rounded-md dark:bg-gray-700 dark:text-gray-200"
            />
          </div>
          <div>
            <label htmlFor="locations" className="block text-gray-700 dark:text-gray-300">
              Preferred Locations
            </label>
            <input
              type="text"
              id="locations"
              name="locations"
              value={formData.locations}
              onChange={handleChange}
              placeholder="e.g. New York, San Francisco"
              className="mt-1 block w-full px-4 py-2 border rounded-md dark:bg-gray-700 dark:text-gray-200"
            />
          </div>
          <div>
            <label htmlFor="salaryExpectations" className="block text-gray-700 dark:text-gray-300">
              Salary Expectations
            </label>
            <input
              type="text"
              id="salaryExpectations"
              name="salaryExpectations"
              value={formData.salaryExpectations}
              onChange={handleChange}
              placeholder="e.g. $80k - $120k"
              className="mt-1 block w-full px-4 py-2 border rounded-md dark:bg-gray-700 dark:text-gray-200"
            />
          </div>
          <div>
            <label htmlFor="languages" className="block text-gray-700 dark:text-gray-300">
              Languages Known
            </label>
            <input
              type="text"
              id="languages"
              name="languages"
              value={formData.languages}
              onChange={handleChange}
              placeholder="e.g. English, Spanish"
              className="mt-1 block w-full px-4 py-2 border rounded-md dark:bg-gray-700 dark:text-gray-200"
            />
          </div>
          <div>
            <label htmlFor="linkedIn" className="block text-gray-700 dark:text-gray-300">
              LinkedIn Profile URL
            </label>
            <input
              type="url"
              id="linkedIn"
              name="linkedIn"
              value={formData.linkedIn}
              onChange={handleChange}
              placeholder="https://www.linkedin.com/in/yourprofile"
              className="mt-1 block w-full px-4 py-2 border rounded-md dark:bg-gray-700 dark:text-gray-200"
            />
          </div>
          <div>
            <label htmlFor="summary" className="block text-gray-700 dark:text-gray-300">
              Professional Summary
            </label>
            <textarea
              id="summary"
              name="summary"
              value={formData.summary}
              onChange={handleChange}
              rows="4"
              placeholder="Write a brief summary about your professional background and career goals"
              className="mt-1 block w-full px-4 py-2 border rounded-md dark:bg-gray-700 dark:text-gray-200"
            ></textarea>
          </div>
          <div>
            <button
              type="submit"
              className="w-full bg-blue-600 hover:bg-blue-700 text-white font-semibold py-3 px-4 rounded-md transition duration-200"
            >
              Submit Profile
            </button>
          </div>
        </form>
      </div>
    </div>
  );
};

export default Job;
