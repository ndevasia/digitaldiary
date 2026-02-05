"use strict";
(function() {
  window.addEventListener("load", init);
  let allMedia = [];

  function init() {
    id('media-filter').addEventListener('change', function () {
      const selectedType = this.value;
      displayMedia(selectedType);
    });
  }
  document.addEventListener('DOMContentLoaded', function () {
    fetchAllMedia();
  });

  function displayMedia(filterType) {
    let mediaList = document.getElementById('media-list');

    // Clear any existing content
    while (mediaList.firstChild) {
        mediaList.removeChild(mediaList.firstChild);
    }

    // Filter media items if a specific type is selected
    let filteredMedia = filterType === 'all'
        ? allMedia
        : allMedia.filter(item => item.type === filterType);

    if (allMedia.length === 0) {
        const noMediaMessage = document.createElement('p');
        noMediaMessage.textContent = 'No media found.';
        mediaList.appendChild(noMediaMessage);
        return;
    }

    // Display each media item
    filteredMedia.forEach(item => {
      const mediaElement = document.createElement('div');
      mediaElement.classList.add('media-item');

      // Display the media itself
      let mediaDisplay;
      if (item.type === 'video') {
          mediaDisplay = document.createElement('video');
          mediaDisplay.controls = true;
          mediaDisplay.src = item.media_url;
      } else if (item.type === 'audio') {
          mediaDisplay = document.createElement('audio');
          mediaDisplay.controls = true;
          mediaDisplay.src = item.media_url;
      } else if (item.type === 'screenshot') {
          mediaDisplay = document.createElement('img');
          mediaDisplay.src = item.media_url;
          mediaDisplay.alt = 'Screenshot';
      }

      mediaElement.appendChild(mediaDisplay);

      // Display the media name
      const nameElement = document.createElement('p');
      nameElement.textContent = `Name: ${item.game}`;
      mediaElement.appendChild(nameElement);

      mediaList.appendChild(mediaElement);
    });
  }

  async function fetchAllMedia() {
    try {
      let response = await fetch('/api/media_aws');
      await statusCheck(response);
      allMedia = await response.json();
      displayMedia('all');
    } catch (err) {
      handleGeneralError();
    }
  }

  function handleGeneralError(err) {
    console.error('An error occurred:', err);

    // Clear existing content in the media list
    const mediaList = document.getElementById('media-list');
    while (mediaList.firstChild) {
        mediaList.removeChild(mediaList.firstChild);
    }

    // Create and append the error message
    const errorMessage = document.createElement('p');
    errorMessage.classList.add('error-message');
    errorMessage.textContent = 'An error occurred while fetching media files. Please try again later.';
    mediaList.appendChild(errorMessage);
  }



  async function statusCheck(res) {
    if (!res.ok) {
      throw new Error(await res.text());
    }
    return res;
  }

  /**
   * Returns the DOM element with the specified ID.
   * @param {string} name - The ID of the DOM element to retrieve.
   * @returns {Element} The DOM element with the specified ID.
   */
  function id(name) {
    return document.getElementById(name);
  }

  /**
   * Returns the first element that matches the specified selector.
   * @param {string} selector - The CSS selector to search for.
   * @returns {Element} The first element that matches the selector.
   */
  function qs(selector) {
    return document.querySelector(selector);
  }

  /**
   * Creates a new DOM element with the specified tag name.
   * @param {string} tagName - The tag name of the element to create.
   * @returns {Element} The newly created DOM element.
   */
  function gen(tagName) {
    return document.createElement(tagName);
  }

  /**
   * Returns all element that matches the specified selector.
   * @param {string} selector - The CSS selector to search for.
   * @returns {NodeListOf<Element>} An array-like NodeList of DOM elements that match the selector.
   */
  function qsa(selector) {
    return document.querySelectorAll(selector);
  }

})();