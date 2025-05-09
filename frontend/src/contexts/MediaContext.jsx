import React, { createContext, useContext, useState, useEffect } from "react";

const MediaContext = createContext();

export function MediaProvider({ children }) {
  const [mediaList, setMediaList] = useState([]);
  const [filteredMedia, setFilteredMedia] = useState([]);
  const [loading, setLoading] = useState(false);
  const [error, setError] = useState(null);
  const [filter, setFilter] = useState("all");
  const [userFilter, setUserFilter] = useState("all");

  const fetchMedia = async () => {
    try {
      setLoading(true);
      const response = await fetch("/api/media");
      if (!response.ok) {
        throw new Error("Failed to fetch media");
      }
      const data = await response.json();
      setMediaList(data);
      setFilteredMedia(data);
      setError(null);
    } catch (error) {
      console.error("Error fetching media:", error);
      setError(error.message);
    } finally {
      setLoading(false);
    }
  };

  useEffect(() => {
    fetchMedia();
  }, []);

  useEffect(() => {
    let filtered = mediaList;

    // Apply media type filter
    if (filter !== "all") {
      filtered = filtered.filter((item) => item.type === filter);
    }

    // Apply user filter
    if (userFilter !== "all") {
      filtered = filtered.filter(
        (item) => item.owner_user_id === parseInt(userFilter)
      );
    }

    setFilteredMedia(filtered);
  }, [filter, userFilter, mediaList]);

  const value = {
    mediaList,
    filteredMedia,
    loading,
    error,
    filter,
    userFilter,
    setFilter,
    setUserFilter,
    fetchMedia,
  };

  return (
    <MediaContext.Provider value={value}>{children}</MediaContext.Provider>
  );
}

export function useMedia() {
  const context = useContext(MediaContext);
  if (context === undefined) {
    throw new Error("useMedia must be used within a MediaProvider");
  }
  return context;
}
