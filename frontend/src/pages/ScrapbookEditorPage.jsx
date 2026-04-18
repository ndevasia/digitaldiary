import React, { useContext, useEffect, useMemo, useState, useRef } from 'react';
import { ChevronLeft, Trash2, Pencil, Check, X, Type, ImageIcon, Plus, MousePointer2, Upload, Download } from 'lucide-react';
import { Link, useParams } from 'react-router-dom';
import { UserContext } from '../context/UserContext';
import { useMediaCache } from '../context/MediaCacheContext.jsx';

const SCRAPBOOKS_KEY = 'digitaldiary.scrapbooks';
const SCRAPBOOK_ITEMS_PREFIX = 'digitaldiary.scrapbook.items.';
const IMAGE_SIZE = { width: 220, height: 220 };
const VIDEO_SIZE = { width: 280, height: 170 };
const TEXT_SIZE = { width: 200, height: 60 };
const CLIPBOARD_FILE_SIZE_LIMIT = 3 * 1024 * 1024;
const STICKER_SIZE = { width: 96, height: 96 };
const PRESET_STICKERS = ['💖', '✨', '🌸', '⭐', '🎮', '🧸', '🌈', '🫶'];

function clamp(value, min, max) {
  return Math.max(min, Math.min(value, max));
}

function getScrapbookById(username, scrapbookId) {
  try {
    const key = `${SCRAPBOOKS_KEY}.${username}`;
    const raw = localStorage.getItem(key);
    const parsed = raw ? JSON.parse(raw) : [];
    return parsed.find((entry) => String(entry.id) === String(scrapbookId)) || null;
  } catch {
    return null;
  }
}

function loadItems(username, scrapbookId) {
  try {
    const key = `${SCRAPBOOK_ITEMS_PREFIX}${username}.${scrapbookId}`;
    const raw = localStorage.getItem(key);
    return raw ? JSON.parse(raw) : [];
  } catch {
    return [];
  }
}

function saveItems(username, scrapbookId, items) {
  try {
    const key = `${SCRAPBOOK_ITEMS_PREFIX}${username}.${scrapbookId}`;
    localStorage.setItem(key, JSON.stringify(items));
    return true;
  } catch {
    return false;
  }
}

function touchScrapbookUpdatedAt(username, scrapbookId) {
  try {
    const key = `${SCRAPBOOKS_KEY}.${username}`;
    const raw = localStorage.getItem(key);
    const parsed = raw ? JSON.parse(raw) : [];
    const next = parsed.map((entry) =>
      String(entry.id) === String(scrapbookId)
        ? { ...entry, updatedAt: new Date().toISOString() }
        : entry
    );
    localStorage.setItem(key, JSON.stringify(next));
  } catch {
    // no-op
  }
}

function updateScrapbookEntry(username, scrapbookId, updater) {
  try {
    const key = `${SCRAPBOOKS_KEY}.${username}`;
    const raw = localStorage.getItem(key);
    const parsed = raw ? JSON.parse(raw) : [];
    const next = parsed.map((entry) => {
      if (String(entry.id) !== String(scrapbookId)) {
        return entry;
      }

      return updater(entry);
    });
    localStorage.setItem(key, JSON.stringify(next));
    return next.find((entry) => String(entry.id) === String(scrapbookId)) || null;
  } catch {
    return null;
  }
}

function createBoardItem(mediaItem, canvasRect, pointerPosition) {
  const isVideo = mediaItem.type === 'video';
  const isSticker = mediaItem.type === 'sticker';
  const isText = mediaItem.type === 'text';
  const size = isSticker ? STICKER_SIZE : isText ? TEXT_SIZE : isVideo ? VIDEO_SIZE : IMAGE_SIZE;
  const x = clamp(pointerPosition.x - size.width / 2, 0, Math.max(0, canvasRect.width - size.width));
  const y = clamp(pointerPosition.y - size.height / 2, 0, Math.max(0, canvasRect.height - size.height));

  return {
    id: `${Date.now()}-${Math.random().toString(16).slice(2)}`,
    mediaId: mediaItem.mediaId || null,
    s3Key: mediaItem.s3Key || null,
    type: isSticker ? 'sticker' : isText ? 'text' : isVideo ? 'video' : 'image',
    url: mediaItem.url,
    name: mediaItem.name,
    sticker: mediaItem.sticker || '',
    width: size.width,
    height: size.height,
    x,
    y
  };
}

function loadImage(src, s3Key) {
  return new Promise(async (resolve, reject) => {
    try {
      let useSrc = src;

      // For S3-hosted images, fetch through our backend proxy to avoid CORS / canvas tainting
      if (s3Key) {
        const resp = await fetch(`/api/proxy-image?key=${encodeURIComponent(s3Key)}`);
        if (resp.ok) {
          const blob = await resp.blob();
          useSrc = URL.createObjectURL(blob);
        }
      }

      const img = new Image();
      img.onload = () => resolve(img);
      img.onerror = (err) => reject(err);
      img.src = useSrc;
    } catch (err) {
      reject(err);
    }
  });
}

function readFileAsDataUrl(file) {
  return new Promise((resolve, reject) => {
    const reader = new FileReader();
    reader.onload = () => resolve(reader.result);
    reader.onerror = reject;
    reader.readAsDataURL(file);
  });
}

function ScrapbookEditorPage() {
  const { scrapbookId } = useParams();
  const API_BASE_URL = import.meta.env.VITE_API_BASE_URL || '';
  const user = useContext(UserContext);
  const currentUsername = user?.username || 'User';
  const apiBasePath = `${API_BASE_URL}/api/${encodeURIComponent(currentUsername)}`;
  const mediaCache = useMediaCache();
  const [scrapbook, setScrapbook] = useState(null);
  const [items, setItems] = useState([]);
  const [hasHydratedItems, setHasHydratedItems] = useState(false);
  const [media, setMedia] = useState([]);
  const [loadingMedia, setLoadingMedia] = useState(true);
  const [mediaError, setMediaError] = useState(null);
  const [draggingItem, setDraggingItem] = useState(null);
  const [selectedItemId, setSelectedItemId] = useState(null);
  const [editingName, setEditingName] = useState(false);
  const [nameValue, setNameValue] = useState('');
  const [resizingItem, setResizingItem] = useState(null);
  const [editingTextId, setEditingTextId] = useState(null);
  const [isLibraryOpen, setIsLibraryOpen] = useState(true);
  const [libraryFilter, setLibraryFilter] = useState('all');
  const [friends, setFriends] = useState([]);
  const [selectedFriends, setSelectedFriends] = useState(new Set([currentUsername]));
  const [loadingFriends, setLoadingFriends] = useState(false);
  const [notice, setNotice] = useState('');
  const canvasRef = useRef(null);
  const uploadInputRef = useRef(null);
  const textEditorRefs = useRef({});
  const noticeTimeoutRef = useRef(null);

  useEffect(() => {
    const found = getScrapbookById(currentUsername, scrapbookId);
    setScrapbook(found ? { ...found, backgroundColor: found.backgroundColor || '#ffffff' } : null);
    setItems(loadItems(currentUsername, scrapbookId));
    setHasHydratedItems(true);
  }, [scrapbookId, currentUsername]);

  useEffect(() => {
    const fetchFriends = async () => {
      try {
        setLoadingFriends(true);
        const response = await fetch(`${apiBasePath}/friends`);
        if (response.ok) {
          const data = await response.json();
          const friendsList = data.friends || [];
          setFriends(friendsList);
        }
      } catch (error) {
        console.error('Error loading friends:', error);
      } finally {
        setLoadingFriends(false);
      }
    };

    fetchFriends();
  }, [apiBasePath]);

  useEffect(() => {
    const fetchMedia = async () => {
      try {
        setLoadingMedia(true);
        setMediaError(null);

        // Fetch media from current user and all selected friends
        const usersToFetch = Array.from(selectedFriends);
        const allMedia = [];

        for (const username of usersToFetch) {
          try {
            // Check cache first
            let data = mediaCache.get(username);
            
            if (!data) {
              // Cache miss, fetch from API
              const response = await fetch(`${API_BASE_URL}/api/${encodeURIComponent(username)}/media_aws`);
              if (response.ok) {
                data = await response.json();
                // Cache the data
                mediaCache.set(username, data);
              }
            }
            
            if (data) {
              // Add username info to each media item for identification
              const mediaWithUser = data.map(item => ({
                ...item,
                owner: username
              }));
              allMedia.push(...mediaWithUser);
            }
          } catch (error) {
            console.error(`Error loading media for user ${username}:`, error);
          }
        }

        const filtered = allMedia.filter((item) => item.type === 'screenshot' || item.type === 'video');
        // Sort by timestamp, most recent first
        const sorted = filtered.sort((a, b) => {
          const timeA = new Date(a.timestamp || 0).getTime();
          const timeB = new Date(b.timestamp || 0).getTime();
          return timeB - timeA;
        });
        setMedia(sorted);
      } catch (error) {
        console.error('Error loading media:', error);
        setMediaError('Could not load photos/videos.');
      } finally {
        setLoadingMedia(false);
      }
    };

    fetchMedia();
  }, [selectedFriends, mediaCache]);

  // Listen for cache invalidation events
  useEffect(() => {
    const handleCacheInvalidation = () => {
      // Invalidate cache for all selected friends
      Array.from(selectedFriends).forEach(username => {
        mediaCache.invalidate(username);
      });
      
      // Refetch media
      const fetchMedia = async () => {
        try {
          setLoadingMedia(true);
          setMediaError(null);

          const usersToFetch = Array.from(selectedFriends);
          const allMedia = [];

          for (const username of usersToFetch) {
            try {
              const response = await fetch(`${API_BASE_URL}/api/${encodeURIComponent(username)}/media_aws`);
              if (response.ok) {
                const data = await response.json();
                mediaCache.set(username, data);
                const mediaWithUser = data.map(item => ({
                  ...item,
                  owner: username
                }));
                allMedia.push(...mediaWithUser);
              }
            } catch (error) {
              console.error(`Error loading media for user ${username}:`, error);
            }
          }

          const filtered = allMedia.filter((item) => item.type === 'screenshot' || item.type === 'video');
          const sorted = filtered.sort((a, b) => {
            const timeA = new Date(a.timestamp || 0).getTime();
            const timeB = new Date(b.timestamp || 0).getTime();
            return timeB - timeA;
          });
          setMedia(sorted);
        } catch (error) {
          console.error('Error loading media:', error);
          setMediaError('Could not load photos/videos.');
        } finally {
          setLoadingMedia(false);
        }
      };

      fetchMedia();
    };

    window.addEventListener('mediaCache:invalidate', handleCacheInvalidation);
    return () => window.removeEventListener('mediaCache:invalidate', handleCacheInvalidation);
  }, [selectedFriends, mediaCache]);

  useEffect(() => {
    if (!scrapbookId || !hasHydratedItems) return;
    if (saveItems(currentUsername, scrapbookId, items)) {
      touchScrapbookUpdatedAt(currentUsername, scrapbookId);
      return;
    }

    setNotice('This scrapbook is too large to save in local storage. Remove some pasted media or use library media instead.');
  }, [items, scrapbookId, hasHydratedItems, currentUsername]);

  useEffect(() => () => {
    if (noticeTimeoutRef.current) {
      window.clearTimeout(noticeTimeoutRef.current);
    }
  }, []);

  useEffect(() => {
    if (!editingTextId) return;

    const target = textEditorRefs.current[editingTextId];
    if (!target) return;

    target.focus();

    const selection = window.getSelection();
    const range = document.createRange();
    range.selectNodeContents(target);
    range.collapse(false);
    selection.removeAllRanges();
    selection.addRange(range);
  }, [editingTextId]);

  const mediaByKey = useMemo(() => {
    const mapped = new Map();
    media.forEach((entry) => {
      if (entry.s3_key) mapped.set(entry.s3_key, entry);
    });
    return mapped;
  }, [media]);

  const mediaById = useMemo(() => {
    const mapped = new Map();
    media.forEach((entry, index) => {
      const id = `${entry.media_id || index}`;
      mapped.set(id, entry);
    });
    return mapped;
  }, [media]);

  const filteredMedia = useMemo(() => {
    if (libraryFilter === 'all') return media;
    if (libraryFilter === 'photos') {
      return media.filter((entry) => entry.type === 'screenshot');
    }
    return media.filter((entry) => entry.type === 'video');
  }, [libraryFilter, media]);

  const showNotice = (message) => {
    setNotice(message);
    if (noticeTimeoutRef.current) {
      window.clearTimeout(noticeTimeoutRef.current);
    }
    noticeTimeoutRef.current = window.setTimeout(() => {
      setNotice('');
    }, 3200);
  };

  const logScrapbookAction = async (actionType, details = {}) => {
    try {
      // Determine which endpoint to use based on action type
      let endpoint;
      switch (actionType) {
        case 'add_media':
          endpoint = `${apiBasePath}/scrapbook/log-add-media`;
          break;
        case 'change_background':
          endpoint = `${apiBasePath}/scrapbook/log-change-background`;
          break;
        case 'add_sticker':
          endpoint = `${apiBasePath}/scrapbook/log-add-sticker`;
          break;
      }

      // Skip if no endpoint matched (shouldn't happen with current action types)
      if (!endpoint) return;

      await fetch(endpoint, {
        method: 'POST',
        headers: {
          'Content-Type': 'application/json',
          'X-User-Secret': localStorage.getItem('auth_token') || ''
        },
        body: JSON.stringify({
          action: actionType,
          scrapbook_id: scrapbookId,
          ...details
        })
      }).catch((err) => {
        // Log silently to avoid disrupting user experience
        console.debug('Scrapbook action logging failed:', err);
      });
    } catch (err) {
      console.debug('Scrapbook action logging error:', err);
    }
  };

  // Refresh presigned URLs for saved items once fresh media is available
  useEffect(() => {
    if (!hasHydratedItems || media.length === 0) return;
    setItems((prev) => {
      let changed = false;
      const next = prev.map((item) => {
        if (item.type === 'text') return item;
        // Match by s3_key (stable) first, then fall back to mediaId
        const fresh = (item.s3Key && mediaByKey.get(item.s3Key)) || mediaById.get(String(item.mediaId));
        if (fresh && fresh.media_url !== item.url) {
          changed = true;
          return { ...item, url: fresh.media_url, s3Key: fresh.s3_key || item.s3Key };
        }
        return item;
      });
      return changed ? next : prev;
    });
  }, [media, hasHydratedItems, mediaByKey, mediaById]);

  const onTrayDragStart = (event, mediaId, s3Key) => {
    event.dataTransfer.setData('text/scrapbook-media-id', String(mediaId));
    if (s3Key) event.dataTransfer.setData('text/scrapbook-s3-key', s3Key);
  };

  const onCanvasDragOver = (event) => {
    event.preventDefault();
  };

  const onCanvasDrop = (event) => {
    event.preventDefault();

    const mediaId = event.dataTransfer.getData('text/scrapbook-media-id');
    const s3Key = event.dataTransfer.getData('text/scrapbook-s3-key');
    if (!mediaId && !s3Key) return;

    const mediaItem = (s3Key && mediaByKey.get(s3Key)) || mediaById.get(String(mediaId));
    if (!mediaItem) return;

    const rect = event.currentTarget.getBoundingClientRect();
    const droppedItem = createBoardItem(
      {
        mediaId,
        s3Key: mediaItem.s3_key || null,
        type: mediaItem.type,
        url: mediaItem.media_url,
        name: mediaItem.game || mediaItem.type
      },
      rect,
      { x: event.clientX - rect.left, y: event.clientY - rect.top }
    );

    setItems((prev) => [...prev, droppedItem]);
    setSelectedItemId(droppedItem.id);
    
    // Log this action to session
    logScrapbookAction('add_media', {
      media_type: mediaItem.type,
      media_id: mediaId || s3Key,
      method: 'drag_drop'
    });
  };

  const addMediaToCanvas = (entry) => {
    const rect = canvasRef.current?.getBoundingClientRect();
    if (!rect) return;

    const nextItem = createBoardItem(
      {
        mediaId: entry.media_id || null,
        s3Key: entry.s3_key || null,
        type: entry.type,
        url: entry.media_url,
        name: entry.game || entry.type
      },
      rect,
      { x: rect.width / 2, y: rect.height / 2 }
    );

    setItems((prev) => [...prev, nextItem]);
    setSelectedItemId(nextItem.id);
    
    // Log this action to session
    logScrapbookAction('add_media', {
      media_type: entry.type,
      media_id: entry.media_id
    });
  };

  const onBoardItemMouseDown = (event, item) => {
    if (item.type === 'text' && editingTextId === item.id) {
      return;
    }

    const canvasRect = event.currentTarget.parentElement.getBoundingClientRect();
    setDraggingItem({
      id: item.id,
      offsetX: event.clientX - canvasRect.left - item.x,
      offsetY: event.clientY - canvasRect.top - item.y
    });
  };

  const onCanvasMouseMove = (event) => {
    if (resizingItem) {
      const rect = event.currentTarget.getBoundingClientRect();
      setItems((prev) =>
        prev.map((item) => {
          if (item.id !== resizingItem.id) return item;
          const newWidth = Math.max(80, event.clientX - rect.left - item.x);
          const newHeight = Math.max(40, event.clientY - rect.top - item.y);
          return { ...item, width: newWidth, height: newHeight };
        })
      );
      return;
    }

    if (!draggingItem) return;

    const rect = event.currentTarget.getBoundingClientRect();

    setItems((prev) =>
      prev.map((item) => {
        if (item.id !== draggingItem.id) return item;

        return {
          ...item,
          x: clamp(event.clientX - rect.left - draggingItem.offsetX, 0, Math.max(0, rect.width - item.width)),
          y: clamp(event.clientY - rect.top - draggingItem.offsetY, 0, Math.max(0, rect.height - item.height))
        };
      })
    );
  };

  const onCanvasMouseUp = () => {
    if (draggingItem) setDraggingItem(null);
    if (resizingItem) setResizingItem(null);
  };

  const onResizeMouseDown = (event, item) => {
    event.stopPropagation();
    setResizingItem({ id: item.id });
  };

  const removeItem = (itemId) => {
    setItems((prev) => prev.filter((i) => i.id !== itemId));
    if (selectedItemId === itemId) setSelectedItemId(null);
    if (editingTextId === itemId) setEditingTextId(null);
  };

  const addTextBox = () => {
    const newItem = {
      id: `${Date.now()}-${Math.random().toString(16).slice(2)}`,
      type: 'text',
      text: 'Double-click to edit',
      width: TEXT_SIZE.width,
      height: TEXT_SIZE.height,
      x: 40,
      y: 40,
      fontSize: 16,
      color: '#374151'
    };
    setItems((prev) => [...prev, newItem]);
    setSelectedItemId(newItem.id);
  };

  const updateTextContent = (itemId, newText) => {
    setItems((prev) =>
      prev.map((item) => (item.id === itemId ? { ...item, text: newText } : item))
    );
  };

  const setBackgroundColor = (color) => {
    const updated = updateScrapbookEntry(currentUsername, scrapbookId, (entry) => ({
      ...entry,
      backgroundColor: color,
      updatedAt: new Date().toISOString()
    }));

    if (updated) {
      setScrapbook((prev) => ({ ...(prev || {}), ...updated }));
      
      // Log this action to session
      logScrapbookAction('change_background', {
        color: color
      });
    }
  };

  const addLocalDecoration = async (file) => {
    if (!file) return;

    if (!file.type.startsWith('image/')) {
      showNotice('Only image files can be added as decorations.');
      return;
    }

    if (file.size > CLIPBOARD_FILE_SIZE_LIMIT) {
      showNotice('That image is too large to save. Choose a smaller decoration image.');
      return;
    }

    const rect = canvasRef.current?.getBoundingClientRect();
    if (!rect) return;

    try {
      const dataUrl = await readFileAsDataUrl(file);
      const nextItem = createBoardItem(
        {
          type: 'image',
          url: dataUrl,
          name: file.name || 'Decoration'
        },
        rect,
        { x: rect.width / 2, y: rect.height / 2 }
      );

      nextItem.width = 140;
      nextItem.height = 140;
      setItems((prev) => [...prev, nextItem]);
      setSelectedItemId(nextItem.id);
      showNotice('Decoration image added.');
      
      // Log this action to session
      logScrapbookAction('add_media', {
        media_type: 'local_decoration',
        file_name: file.name || 'Decoration',
        method: 'local_upload'
      });
    } catch {
      showNotice('Could not add that image.');
    }
  };

  const addSticker = (sticker) => {
    const rect = canvasRef.current?.getBoundingClientRect();
    if (!rect) return;

    const nextItem = createBoardItem(
      {
        type: 'sticker',
        sticker,
        name: 'Sticker'
      },
      rect,
      { x: rect.width / 2, y: rect.height / 2 }
    );

    setItems((prev) => [...prev, nextItem]);
    setSelectedItemId(nextItem.id);
    
    // Log this action to session
    logScrapbookAction('add_sticker', {
      sticker: sticker
    });
  };

  const startRenamingScrapbook = () => {
    setNameValue(scrapbook.name);
    setEditingName(true);
  };

  const confirmRenameScrapbook = () => {
    if (!nameValue.trim()) return;
    const updated = updateScrapbookEntry(currentUsername, scrapbookId, (entry) => ({
      ...entry,
      name: nameValue.trim(),
      updatedAt: new Date().toISOString()
    }));
    if (updated) {
      setScrapbook((prev) => ({ ...prev, ...updated }));
    }
    setEditingName(false);
  };

  const cancelRenameScrapbook = () => {
    setEditingName(false);
  };

  const onCanvasClick = (event) => {
    setEditingTextId(null);
    if (event.target === event.currentTarget) {
      setSelectedItemId(null);
    }
  };

  const clearBoard = () => {
    setItems([]);
    setSelectedItemId(null);
    setEditingTextId(null);
  };

  useEffect(() => {
    const handlePaste = async (event) => {
      const activeElement = document.activeElement;
      const isTypingTarget = activeElement && (
        activeElement.tagName === 'INPUT' ||
        activeElement.tagName === 'TEXTAREA' ||
        activeElement.isContentEditable
      );

      if (isTypingTarget || !canvasRef.current) {
        return;
      }

      const clipboardItems = Array.from(event.clipboardData?.items || []);
      const fileItem = clipboardItems.find((item) => item.kind === 'file' && (item.type.startsWith('image/') || item.type.startsWith('video/')));

      if (!fileItem) {
        return;
      }

      const file = fileItem.getAsFile();
      if (!file) {
        return;
      }

      if (file.size > CLIPBOARD_FILE_SIZE_LIMIT) {
        showNotice('Clipboard media is too large to save. Use the media library for larger files.');
        return;
      }

      event.preventDefault();

      try {
        const dataUrl = await readFileAsDataUrl(file);
        const rect = canvasRef.current.getBoundingClientRect();
        const clipboardItem = createBoardItem(
          {
            type: file.type.startsWith('video/') ? 'video' : 'image',
            url: dataUrl,
            name: file.name || 'Clipboard item'
          },
          rect,
          { x: rect.width / 2, y: rect.height / 2 }
        );

        setItems((prev) => [...prev, clipboardItem]);
        setSelectedItemId(clipboardItem.id);
        showNotice('Clipboard media added to your scrapbook.');
      } catch {
        showNotice('Could not read clipboard media.');
      }
    };

    window.addEventListener('paste', handlePaste);
    return () => window.removeEventListener('paste', handlePaste);
  }, []);

  if (!scrapbook) {
    return (
      <div className="flex-1 p-8">
        <Link to="/scrapbook" className="inline-flex items-center text-teal-500 hover:text-teal-600 mb-4">
          <ChevronLeft size={18} className="mr-1" />
          Back to scrapbooks
        </Link>
        <div className="bg-white border border-gray-200 rounded-lg p-6 text-gray-600">Scrapbook not found.</div>
      </div>
    );
  }

  return (
    <div className="flex-1 overflow-hidden bg-gray-100 p-6">
      <div className="mb-4 flex items-center justify-between">
        <div>
          <Link to="/scrapbook" className="inline-flex items-center text-teal-500 hover:text-teal-600 mb-2">
            <ChevronLeft size={18} className="mr-1" />
            Back to scrapbooks
          </Link>
          {editingName ? (
            <div className="flex items-center gap-2">
              <input
                type="text"
                value={nameValue}
                onChange={(e) => setNameValue(e.target.value)}
                onKeyDown={(e) => {
                  if (e.key === 'Enter') confirmRenameScrapbook();
                  if (e.key === 'Escape') cancelRenameScrapbook();
                }}
                className="text-2xl font-semibold text-gray-800 border-b-2 border-teal-400 bg-transparent focus:outline-none"
                autoFocus
              />
              <button onClick={confirmRenameScrapbook} className="text-green-600 hover:text-green-700">
                <Check size={18} />
              </button>
              <button onClick={cancelRenameScrapbook} className="text-gray-400 hover:text-gray-600">
                <X size={18} />
              </button>
            </div>
          ) : (
            <div className="flex items-center gap-2">
              <h1 className="text-2xl font-semibold text-gray-800">{scrapbook.name}</h1>
              <button
                onClick={startRenamingScrapbook}
                className="p-1 rounded hover:bg-gray-100 text-gray-400 hover:text-teal-500"
                title="Rename scrapbook"
              >
                <Pencil size={14} />
              </button>
            </div>
          )}
        </div>
        <div className="flex items-center gap-2">
          <label className="flex items-center gap-2 rounded border border-gray-200 bg-white px-3 py-2 text-sm text-gray-700 shadow-sm">
            Background
            <input
              type="color"
              value={scrapbook.backgroundColor || '#ffffff'}
              onChange={(e) => setBackgroundColor(e.target.value)}
              className="h-7 w-10 cursor-pointer rounded border-0 bg-transparent p-0"
            />
          </label>
          <button
            type="button"
            onClick={() => uploadInputRef.current?.click()}
            className="px-4 py-2 rounded border border-gray-200 bg-white text-sm text-gray-700 hover:bg-gray-50 flex items-center gap-2 shadow-sm"
          >
            <Upload size={14} />
            Add decoration
          </button>
          <button
            type="button"
            onClick={() => setIsLibraryOpen((prev) => !prev)}
            className="px-4 py-2 rounded border border-gray-200 bg-white text-sm text-gray-700 hover:bg-gray-50 flex items-center gap-2 shadow-sm"
          >
            <ImageIcon size={16} />
            {isLibraryOpen ? 'Hide library' : 'Open library'}
          </button>
          <button
            type="button"
            onClick={addTextBox}
            className="px-4 py-2 rounded border border-gray-200 bg-white text-sm text-gray-700 hover:bg-gray-50 flex items-center gap-1 shadow-sm"
          >
            <Type size={14} />
            Add text
          </button>
          <button
            type="button"
            onClick={clearBoard}
            className="px-4 py-2 rounded border border-gray-200 bg-white text-sm text-gray-700 hover:bg-gray-50 shadow-sm"
          >
            Clear board
          </button>
        </div>
      </div>

      <div className="mb-4 flex items-center gap-2 overflow-x-auto">
        <div className="text-sm text-gray-600 whitespace-nowrap">Preset stickers</div>
        {PRESET_STICKERS.map((sticker) => (
          <button
            key={sticker}
            type="button"
            onClick={() => addSticker(sticker)}
            className="flex h-10 w-10 items-center justify-center rounded-full border border-gray-200 bg-white text-xl shadow-sm transition hover:bg-gray-50"
            title={`Add ${sticker} sticker`}
          >
            {sticker}
          </button>
        ))}
      </div>

      <input
        ref={uploadInputRef}
        type="file"
        accept="image/*"
        className="hidden"
        onChange={async (e) => {
          const file = e.target.files?.[0];
          await addLocalDecoration(file);
          e.target.value = '';
        }}
      />

      {notice && (
        <div className="mb-4 rounded border border-amber-200 bg-amber-50 px-4 py-3 text-sm text-amber-800 shadow-sm">
          {notice}
        </div>
      )}

      <div className="relative h-[79vh] overflow-hidden rounded-lg border border-gray-200 bg-white p-3 shadow-sm">
        <div
          ref={canvasRef}
          className="relative h-full w-full overflow-hidden rounded-lg border border-dashed border-gray-300"
          style={{ backgroundColor: scrapbook.backgroundColor || '#ffffff' }}
          onDragOver={onCanvasDragOver}
          onDrop={onCanvasDrop}
          onMouseMove={onCanvasMouseMove}
          onMouseUp={onCanvasMouseUp}
          onMouseLeave={onCanvasMouseUp}
          onClick={onCanvasClick}
        >
          {items.length === 0 && (
            <div className="absolute inset-0 flex flex-col items-center justify-center gap-3 text-gray-400 text-sm">
              <div className="rounded-full bg-gray-100 p-3 text-gray-500">
                <MousePointer2 size={24} />
              </div>
              <div className="text-center">
                Drag photos or videos from the library onto this blank page.
                <br />
                You can also click media to add it or paste an image from your clipboard.
              </div>
            </div>
          )}

          {items.map((item) => (
            <div
              key={item.id}
              data-item-id={item.id}
              className={`absolute cursor-grab active:cursor-grabbing group/item ${
                selectedItemId === item.id ? 'ring-2 ring-teal-400 rounded-xl' : ''
              }`}
              style={{ left: item.x, top: item.y, width: item.width, height: item.height }}
              onMouseDown={(event) => {
                setSelectedItemId(item.id);
                onBoardItemMouseDown(event, item);
              }}
            >
              {/* Delete button */}
              <button
                className="absolute -top-3 -right-3 z-10 bg-red-500 text-white rounded-full p-0.5
                           opacity-0 group-hover/item:opacity-100 transition-opacity shadow"
                onClick={(e) => {
                  e.stopPropagation();
                  removeItem(item.id);
                }}
                title="Remove"
              >
                <Trash2 size={12} />
              </button>

              {item.type === 'video' ? (
                <video src={item.url} controls className="w-full h-full rounded-xl shadow object-cover" />
              ) : item.type === 'sticker' ? (
                <div
                  className="flex h-full w-full items-center justify-center rounded-xl bg-transparent leading-none select-none"
                  style={{ fontSize: `${Math.max(32, Math.min(item.width, item.height) * 0.72)}px` }}
                >
                  {item.sticker}
                </div>
              ) : item.type === 'text' ? (
                <div
                  ref={(node) => {
                    if (node) {
                      textEditorRefs.current[item.id] = node;
                    } else {
                      delete textEditorRefs.current[item.id];
                    }
                  }}
                  className={`w-full h-full rounded-xl bg-yellow-50 border border-yellow-200 shadow p-2 text-sm overflow-auto ${
                    editingTextId === item.id ? 'cursor-text' : 'cursor-grab select-none'
                  }`}
                  contentEditable={editingTextId === item.id}
                  suppressContentEditableWarning
                  style={{ fontSize: item.fontSize, color: item.color }}
                  onBlur={(e) => {
                    updateTextContent(item.id, e.currentTarget.textContent || '');
                    setEditingTextId(null);
                  }}
                  onDoubleClick={(e) => {
                    e.stopPropagation();
                    setEditingTextId(item.id);
                    setSelectedItemId(item.id);
                  }}
                  onMouseDown={(e) => {
                    if (editingTextId === item.id) {
                      e.stopPropagation();
                    }
                  }}
                >
                  {item.text}
                </div>
              ) : (
                <img src={item.url} alt={item.name} className="w-full h-full rounded-xl shadow object-cover" draggable={false} />
              )}

              {/* Resize handle */}
              <div
                className="absolute bottom-0 right-0 w-4 h-4 cursor-nwse-resize
                           opacity-0 group-hover/item:opacity-100 transition-opacity"
                onMouseDown={(event) => onResizeMouseDown(event, item)}
              >
                <svg width="16" height="16" viewBox="0 0 16 16" className="text-gray-400">
                  <path d="M14 14L8 14M14 14L14 8M14 14L6 6" stroke="currentColor" strokeWidth="1.5" fill="none" />
                </svg>
              </div>
            </div>
          ))}
        </div>

        {isLibraryOpen && (
          <aside className="absolute right-6 top-6 bottom-6 z-20 flex w-80 flex-col rounded-lg border border-gray-200 bg-white p-4 shadow-lg">
            <div className="mb-4 flex items-start justify-between gap-3">
              <div>
                <h2 className="text-lg font-semibold text-gray-800">Media library</h2>
                <p className="text-xs text-gray-500">Drag onto the page or click to place in the center.</p>
              </div>
              <button
                type="button"
                onClick={() => setIsLibraryOpen(false)}
                className="rounded-full border border-gray-200 p-2 text-gray-500 hover:bg-gray-50"
                title="Close library"
              >
                <X size={14} />
              </button>
            </div>

            <div className="mb-4 space-y-3">
              <div className="flex gap-2">
                {[
                  { value: 'all', label: 'All' },
                  { value: 'photos', label: 'Photos' },
                  { value: 'videos', label: 'Videos' }
                ].map((option) => (
                  <button
                    key={option.value}
                    type="button"
                    onClick={() => setLibraryFilter(option.value)}
                    className={`rounded-full px-3 py-1.5 text-xs font-medium transition ${
                      libraryFilter === option.value
                        ? 'bg-teal-500 text-white'
                        : 'bg-gray-100 text-gray-600 hover:bg-gray-200'
                    }`}
                  >
                    {option.label}
                  </button>
                ))}
              </div>

              <div>
                <label className="block text-xs font-medium text-gray-600 mb-2">Users</label>
                <div className="space-y-1 max-h-32 overflow-y-auto">
                  <label className="flex items-center gap-2 cursor-pointer hover:bg-gray-50 p-2 rounded">
                    <input
                      type="checkbox"
                      checked={selectedFriends.has(currentUsername)}
                      onChange={(e) => {
                        const newSelected = new Set(selectedFriends);
                        if (e.target.checked) {
                          newSelected.add(currentUsername);
                        } else {
                          newSelected.delete(currentUsername);
                        }
                        setSelectedFriends(newSelected);
                      }}
                      className="rounded"
                    />
                    <span className="text-xs text-gray-700">{currentUsername} (You)</span>
                  </label>

                  {friends.map((friend) => (
                    <label key={friend} className="flex items-center gap-2 cursor-pointer hover:bg-gray-50 p-2 rounded">
                      <input
                        type="checkbox"
                        checked={selectedFriends.has(friend)}
                        onChange={(e) => {
                          const newSelected = new Set(selectedFriends);
                          if (e.target.checked) {
                            newSelected.add(friend);
                          } else {
                            newSelected.delete(friend);
                          }
                          setSelectedFriends(newSelected);
                        }}
                        className="rounded"
                      />
                      <span className="text-xs text-gray-700">{friend}</span>
                    </label>
                  ))}

                  {friends.length === 0 && (
                    <div className="text-xs text-gray-400 p-2">No friends yet</div>
                  )}
                </div>
              </div>
            </div>

            {loadingMedia && <div className="text-sm text-gray-500">Loading media...</div>}
            {mediaError && <div className="text-sm text-red-500">{mediaError}</div>}

            {!loadingMedia && !mediaError && filteredMedia.length === 0 && (
              <div className="rounded-2xl border border-dashed border-gray-200 bg-gray-50 px-4 py-8 text-center text-sm text-gray-500">
                No matching photos or videos found yet.
              </div>
            )}

            <div className="grid flex-1 grid-cols-1 gap-3 overflow-y-auto pr-1">
              {filteredMedia.map((entry, index) => {
                const mediaId = `${entry.media_id || index}`;
                const isVideo = entry.type === 'video';

                return (
                  <button
                    key={`${mediaId}-${entry.media_url}`}
                    type="button"
                    className="cursor-grab rounded-2xl border border-gray-200 bg-gray-50 p-2 text-left transition hover:border-teal-300 hover:bg-teal-50"
                    draggable
                    onDragStart={(event) => onTrayDragStart(event, mediaId, entry.s3_key)}
                    onClick={() => addMediaToCanvas(entry)}
                  >
                    {isVideo ? (
                      <div className="relative h-28 w-full rounded-xl bg-gray-900 flex items-center justify-center overflow-hidden">
                        <video 
                          src={entry.media_url} 
                          className="w-full h-full object-cover"
                          preload="metadata"
                          muted
                        />
                        <div className="absolute inset-0 flex items-center justify-center bg-black/30 pointer-events-none">
                          <svg className="w-8 h-8 text-white" fill="currentColor" viewBox="0 0 20 20">
                            <path d="M6.3 2.841A1.5 1.5 0 004 4.11V15.89a1.5 1.5 0 002.3 1.269l9.344-5.89a1.5 1.5 0 000-2.538L6.3 2.84z" />
                          </svg>
                        </div>
                      </div>
                    ) : (
                      <img src={entry.media_url} alt={entry.game || 'Photo'} className="h-28 w-full rounded-xl object-cover" draggable={false} />
                    )}
                    <div className="mt-2 space-y-1">
                      <div className="flex items-center justify-between">
                        <div className="truncate text-xs font-medium text-gray-700">{entry.game || (isVideo ? 'Video' : 'Photo')}</div>
                        <span className="inline-flex items-center gap-1 rounded-full bg-white px-2 py-1 text-[10px] uppercase tracking-[0.18em] text-gray-500">
                          <Plus size={10} />
                          Add
                        </span>
                      </div>
                      <div className="space-y-0.5">
                        <div className="truncate text-xs text-gray-500">
                          {entry.owner === currentUsername ? 'Your media' : `From ${entry.owner}`}
                        </div>
                        {entry.timestamp && (
                          <div className="truncate text-xs text-gray-400">
                            {new Date(entry.timestamp).toLocaleString()}
                          </div>
                        )}
                      </div>
                    </div>
                  </button>
                );
              })}
            </div>
          </aside>
        )}

        {/* Save / Export button */}
        <button
          type="button"
          onClick={async () => {
            const canvas = canvasRef.current;
            if (!canvas) return;
            const rect = canvas.getBoundingClientRect();
            const offscreen = document.createElement('canvas');
            offscreen.width = rect.width;
            offscreen.height = rect.height;
            const ctx = offscreen.getContext('2d');

            ctx.fillStyle = scrapbook.backgroundColor || '#ffffff';
            ctx.fillRect(0, 0, offscreen.width, offscreen.height);

            for (const item of items) {
              if (item.type === 'text') {
                // Draw rounded rectangle background with border (text bubble styling)
                const radius = 12;
                const padding = 8;
                ctx.fillStyle = '#fffbeb'; // Light yellow background
                ctx.fillRect(item.x + radius, item.y, item.width - 2 * radius, item.height);
                ctx.fillRect(item.x, item.y + radius, item.width, item.height - 2 * radius);
                
                // Draw corners with arc
                ctx.beginPath();
                ctx.moveTo(item.x + radius, item.y);
                ctx.arcTo(item.x, item.y, item.x, item.y + radius, radius);
                ctx.arcTo(item.x, item.y + item.height, item.x + radius, item.y + item.height, radius);
                ctx.arcTo(item.x + item.width, item.y + item.height, item.x + item.width, item.y + item.height - radius, radius);
                ctx.arcTo(item.x + item.width, item.y, item.x + item.width - radius, item.y, radius);
                ctx.closePath();
                ctx.fill();
                
                // Draw border
                ctx.strokeStyle = '#fcd34d'; // Yellow border
                ctx.lineWidth = 1;
                ctx.stroke();
                
                // Draw text on top
                ctx.font = `${item.fontSize || 16}px sans-serif`;
                ctx.fillStyle = item.color || '#374151';
                const lines = (item.text || '').split('\n');
                const lineHeight = (item.fontSize || 16) * 1.3;
                lines.forEach((line, i) => {
                  ctx.fillText(line, item.x + padding, item.y + padding + (item.fontSize || 16) + i * lineHeight);
                });
              } else if (item.type === 'sticker') {
                const size = Math.max(32, Math.min(item.width, item.height) * 0.72);
                ctx.font = `${size}px sans-serif`;
                ctx.textAlign = 'center';
                ctx.textBaseline = 'middle';
                ctx.fillText(item.sticker, item.x + item.width / 2, item.y + item.height / 2);
                ctx.textAlign = 'start';
                ctx.textBaseline = 'alphabetic';
              } else if (item.type === 'image' && item.url) {
                try {
                  const img = await loadImage(item.url, item.s3Key);
                  ctx.drawImage(img, item.x, item.y, item.width, item.height);
                } catch {
                  // skip images that fail to load
                }
              } else if (item.type === 'video' && item.url) {
                ctx.fillStyle = '#1a1a2e';
                ctx.fillRect(item.x, item.y, item.width, item.height);
                ctx.fillStyle = '#ffffff';
                ctx.font = '14px sans-serif';
                ctx.textAlign = 'center';
                ctx.fillText('\u25b6 Video', item.x + item.width / 2, item.y + item.height / 2);
                ctx.textAlign = 'start';
              }
            }

            const link = document.createElement('a');
            link.download = `${scrapbook.name || 'scrapbook'}.png`;
            link.href = offscreen.toDataURL('image/png');
            link.click();
            showNotice('Scrapbook exported as image!');
          }}
          className="absolute bottom-6 right-6 z-30 px-5 py-3 rounded-2xl bg-teal-500 text-sm font-medium text-white hover:bg-teal-600 flex items-center gap-2 shadow-lg transition"
        >
          <Download size={16} />
          Save
        </button>
      </div>
    </div>
  );
}

export default ScrapbookEditorPage;
