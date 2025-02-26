// Jobl.jsx
import React from 'react';
import { useLocation, useNavigate } from 'react-router-dom';

const Jobl = () => {
  const location = useLocation();
  const navigate = useNavigate();

  // Retrieve the generated query and job results passed via location.state.
  // Expecting jobResults to be an array containing the API response.
  const generatedQuery = location.state?.generatedQuery || "";
  const jobResultsFromState = location.state?.jobResults || [];

  // If no valid data, display a fallback message.
  if (!generatedQuery || jobResultsFromState.length === 0) {
    return (
      <div className="min-h-screen flex flex-col items-center justify-center bg-gray-100 dark:bg-gray-900 p-8">
        <p className="text-gray-700 dark:text-gray-300">
          No job results found. Please submit your profile first.
        </p>
        <button
          onClick={() => navigate(-1)}
          className="mt-4 bg-blue-600 hover:bg-blue-700 text-white px-4 py-2 rounded"
        >
          Back to Profile
        </button>
      </div>
    );
  }

  // Map the API response to our display format.
  // If the job object contains a "data" property, use that.
  const jobObjects = jobResultsFromState.map(job => {
    const jobData = job.data || job; // in case it's already the job details
    return {
      link: jobData.url || "#",
      title: jobData.title || "Job Title Not Provided",
      company: (jobData.company && jobData.company.name) || "Company Not Provided",
      location: jobData.location || "Location Not Provided",
      description: jobData.description || "No description available.",
      // Use a generic thumbnail as the API doesn't provide one.
      thumbnail: jobData.thumbnail || "https://images.unsplash.com/photo-1504384308090-c894fdcc538d?ixlib=rb-1.2.1&auto=format&fit=crop&w=300&q=80"
    };
  });

  // For demonstration, we show only the first job in the array.
  const job = jobObjects[0];

  return (
    <div className="min-h-screen bg-gray-100 dark:bg-gray-900 p-8">
      <button
        onClick={() => navigate("/Job")}
        className="mb-4 bg-gray-200 hover:bg-gray-300 text-gray-800 px-4 py-2 rounded"
      >
        Back
      </button>
      <div className="bg-white dark:bg-gray-800 rounded-lg shadow-md p-6">
        <img
          src={job.thumbnail}
          alt={job.title}
          className="w-full h-48 object-cover rounded-md"
        />
        <h1 className="text-3xl font-bold mt-4 text-gray-800 dark:text-gray-100">
          {job.title}
        </h1>
        <p className="text-lg text-gray-600 dark:text-gray-300 mt-2">
          {job.company}
        </p>
        <p className="text-md text-gray-600 dark:text-gray-300 mt-2">
          {job.location}
        </p>
        <div className="mt-4 text-gray-700 dark:text-gray-300">
          <p>{job.description}</p>
        </div>
        <a
          href={job.link}
          target="_blank"
          rel="noopener noreferrer"
          className="mt-4 inline-block bg-blue-600 hover:bg-blue-700 text-white px-4 py-2 rounded"
        >
          View Full Job Details
        </a>
      </div>
    </div>
  );
};

export default Jobl;
