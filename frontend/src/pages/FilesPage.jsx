import React, { useState } from "react";
import { ChevronDown } from "lucide-react";
import Sidebar from "../components/Sidebar";
import { useUsers } from "../contexts/UserContext";
import { useMedia } from "../contexts/MediaContext";

function FilesPage() {
  const [showDropdown, setShowDropdown] = useState(false);
  const { users } = useUsers();
  const {
    filteredMedia,
    loading,
    error,
    filter,
    userFilter,
    setFilter,
    setUserFilter,
    fetchMedia,
  } = useMedia();

  const handleFilterChange = (filterType) => {
    setFilter(filterType);
    setShowDropdown(false);
  };

  const getFilterDisplayName = (filterType) => {
    switch (filterType) {
      case "all":
        return "All";
      case "screenshot":
        return "Screenshots";
      case "audio":
        return "Audio";
      case "video":
        return "Video";
      default:
        return "All";
    }
  };

  const renderMediaItem = (item) => {
    // Format the timestamp
    const formatDate = (timestamp) => {
      if (!timestamp) return "Jan 1, 2023"; // Default date if none available
      const date = new Date(timestamp);
      return date.toLocaleDateString("en-US", {
        month: "short",
        day: "numeric",
        year: "numeric",
      });
    };

    // Determine background color based on media type
    let mediaClass = "";
    switch (item.type) {
      case "video":
        mediaClass = "bg-pink-200";
        break;
      case "screenshot":
        mediaClass = "bg-blue-100";
        break;
      case "audio":
        mediaClass = "bg-green-200";
        break;
      default:
        mediaClass = "bg-blue-100";
    }

    switch (item.type) {
      case "video":
        return (
          <div className="h-full flex flex-col">
            <div
              className={`${mediaClass} rounded overflow-hidden shadow-sm p-4 flex-grow flex justify-center items-center`}
            >
              <video controls className="w-full rounded">
                <source src={item.media_url} type="video/mp4" />
                Your browser does not support the video tag.
              </video>
            </div>
            <div className="mt-2">
              <div className="font-medium text-gray-700">{item.game}</div>
              <div className="text-xs text-gray-500">
                {formatDate(item.timestamp)}
              </div>
            </div>
          </div>
        );
      case "audio":
        return (
          <div className="h-full flex flex-col">
            <div
              className={`${mediaClass} rounded overflow-hidden shadow-sm p-4 flex-grow flex justify-center items-center`}
            >
              <audio controls className="w-full">
                <source src={item.media_url} type="audio/mpeg" />
                Your browser does not support the audio tag.
              </audio>
            </div>
            <div className="mt-2">
              <div className="font-medium text-gray-700">{item.game}</div>
              <div className="text-xs text-gray-500">
                {formatDate(item.timestamp)}
              </div>
            </div>
          </div>
        );
      case "screenshot":
        return (
          <div className="h-full flex flex-col">
            <div
              className={`${mediaClass} rounded overflow-hidden shadow-sm p-4 flex-grow flex justify-center items-center`}
            >
              <img
                src={item.media_url}
                alt="Screenshot"
                className="w-full rounded"
              />
            </div>
            <div className="mt-2">
              <div className="font-medium text-gray-700">{item.game}</div>
              <div className="text-xs text-gray-500">
                {formatDate(item.timestamp)}
              </div>
            </div>
          </div>
        );
      default:
        return null;
    }
  };

  return (
    <div className="flex h-screen bg-blue-50">
      <Sidebar />

      <div className="flex-1 p-8 overflow-y-auto">
        <header className="flex justify-between items-center mb-6">
          <h1 className="text-2xl font-semibold text-gray-700">
            Hello, {users.map((user) => user.username).join(" & ")}
          </h1>
        </header>

        <div className="bg-white rounded-lg border border-gray-200 p-8">
          <h2 className="text-xl font-medium text-gray-700 mb-4">Files</h2>

          {/* Filters Section */}
          <div className="mb-8 flex justify-between items-center">
            {/* User Filter Tabs */}
            <div className="flex flex-wrap gap-2">
              {users.map((user) => (
                <button
                  key={user.user_id}
                  onClick={() => setUserFilter(user.user_id)}
                  className={`px-4 py-2 rounded-full text-sm font-medium transition-colors duration-200 ${
                    userFilter === user.user_id
                      ? "bg-teal-500 text-white"
                      : "bg-gray-100 text-gray-600 hover:bg-gray-200"
                  }`}
                >
                  {user.username}
                </button>
              ))}
            </div>

            {/* Media Filter Dropdown */}
            <div className="relative">
              <button
                className="bg-teal-500 text-white px-4 py-2 rounded flex items-center"
                onClick={() => setShowDropdown(!showDropdown)}
              >
                {getFilterDisplayName(filter)}{" "}
                <ChevronDown size={18} className="ml-2" />
              </button>

              {showDropdown && (
                <div className="absolute top-full right-0 mt-1 bg-white shadow-md rounded-lg border border-gray-200 w-40 z-10">
                  <ul>
                    <li
                      className="px-4 py-2 hover:bg-gray-100 text-teal-500 cursor-pointer"
                      onClick={() => handleFilterChange("all")}
                    >
                      All
                    </li>
                    <li
                      className="px-4 py-2 hover:bg-gray-100 text-teal-500 cursor-pointer"
                      onClick={() => handleFilterChange("screenshot")}
                    >
                      Screenshots
                    </li>
                    <li
                      className="px-4 py-2 hover:bg-gray-100 text-teal-500 cursor-pointer"
                      onClick={() => handleFilterChange("audio")}
                    >
                      Audio
                    </li>
                    <li
                      className="px-4 py-2 hover:bg-gray-100 text-teal-500 cursor-pointer"
                      onClick={() => handleFilterChange("video")}
                    >
                      Video
                    </li>
                  </ul>
                </div>
              )}
            </div>
          </div>

          {loading ? (
            <div className="grid grid-cols-3 gap-6">
              {[1, 2, 3, 4, 5, 6].map((_, index) => (
                <div
                  key={index}
                  className="animate-pulse bg-blue-100 h-48 rounded"
                ></div>
              ))}
            </div>
          ) : error ? (
            <div className="text-center py-12">
              <p className="text-red-500">{error}</p>
              <button
                className="mt-4 bg-teal-500 text-white px-4 py-2 rounded hover:bg-teal-600"
                onClick={fetchMedia}
              >
                Try Again
              </button>
            </div>
          ) : filteredMedia.length === 0 ? (
            <div className="text-center py-12">
              <p className="text-gray-500">No media files found.</p>
            </div>
          ) : (
            <div className="grid grid-cols-1 md:grid-cols-3 gap-6">
              {filteredMedia.map((item) => (
                <div
                  key={item.media_id}
                  className="bg-white rounded-lg shadow-sm overflow-hidden p-4 flex flex-col"
                >
                  <div className="flex-grow">{renderMediaItem(item)}</div>
                </div>
              ))}
            </div>
          )}
        </div>
      </div>
    </div>
  );
}

export default FilesPage;
