import React, { useEffect, useMemo, useState } from 'react';
import { useNavigate } from 'react-router-dom';
import { Trash2, Pencil, Check, X, Plus, ArrowRight } from 'lucide-react';

const SCRAPBOOKS_KEY = 'digitaldiary.scrapbooks';
const SCRAPBOOK_ITEMS_PREFIX = 'digitaldiary.scrapbook.items.';

function readScrapbooks() {
  try {
    const raw = localStorage.getItem(SCRAPBOOKS_KEY);
    const parsed = raw ? JSON.parse(raw) : [];
    return Array.isArray(parsed) ? parsed : [];
  } catch {
    return [];
  }
}

function writeScrapbooks(scrapbooks) {
  localStorage.setItem(SCRAPBOOKS_KEY, JSON.stringify(scrapbooks));
}

function getScrapbookItemCount(scrapbookId) {
  try {
    const raw = localStorage.getItem(`${SCRAPBOOK_ITEMS_PREFIX}${scrapbookId}`);
    const parsed = raw ? JSON.parse(raw) : [];
    return Array.isArray(parsed) ? parsed.length : 0;
  } catch {
    return 0;
  }
}

function ScrapbookPage() {
  const navigate = useNavigate();
  const [scrapbooks, setScrapbooks] = useState([]);
  const [editingId, setEditingId] = useState(null);
  const [editingName, setEditingName] = useState('');

  useEffect(() => {
    setScrapbooks(readScrapbooks());
  }, []);

  const sortedScrapbooks = useMemo(
    () => [...scrapbooks].sort((a, b) => new Date(b.updatedAt || b.createdAt) - new Date(a.updatedAt || a.createdAt)),
    [scrapbooks]
  );

  const scrapbookCards = useMemo(
    () => sortedScrapbooks.map((scrapbook) => ({ ...scrapbook, itemCount: getScrapbookItemCount(scrapbook.id) })),
    [sortedScrapbooks]
  );

  const createNewScrapbook = () => {
    const nowIso = new Date().toISOString();
    const nextIndex = scrapbooks.length + 1;
    const newScrapbook = {
      id: `${Date.now()}-${Math.random().toString(16).slice(2)}`,
      name: `Scrapbook ${nextIndex}`,
      createdAt: nowIso,
      updatedAt: nowIso
    };

    const next = [newScrapbook, ...scrapbooks];
    setScrapbooks(next);
    writeScrapbooks(next);
    navigate(`/scrapbook/${newScrapbook.id}`);
  };

  const openScrapbook = (id) => {
    navigate(`/scrapbook/${id}`);
  };

  const deleteScrapbook = (e, id) => {
    e.stopPropagation();
    const next = scrapbooks.filter((s) => s.id !== id);
    setScrapbooks(next);
    writeScrapbooks(next);
    // Also remove the scrapbook's items
    localStorage.removeItem(`${SCRAPBOOK_ITEMS_PREFIX}${id}`);
  };

  const startRename = (e, scrapbook) => {
    e.stopPropagation();
    setEditingId(scrapbook.id);
    setEditingName(scrapbook.name);
  };

  const confirmRename = (e) => {
    e.stopPropagation();
    if (!editingName.trim()) return;
    const next = scrapbooks.map((s) =>
      s.id === editingId ? { ...s, name: editingName.trim(), updatedAt: new Date().toISOString() } : s
    );
    setScrapbooks(next);
    writeScrapbooks(next);
    setEditingId(null);
    setEditingName('');
  };

  const cancelRename = (e) => {
    e.stopPropagation();
    setEditingId(null);
    setEditingName('');
  };

  return (
    <div className="flex-1 overflow-auto bg-[radial-gradient(circle_at_top,_rgba(20,184,166,0.14),_transparent_45%),linear-gradient(180deg,_#f0fdfa_0%,_#eff6ff_100%)] p-8">
      <section className="rounded-[28px] border border-white/70 bg-white/85 shadow-sm backdrop-blur px-8 py-8 mb-8">
        <div className="flex flex-col gap-6 lg:flex-row lg:items-end lg:justify-between">
          <div className="max-w-2xl">
            <div className="inline-flex items-center rounded-full bg-teal-50 px-3 py-1 text-xs font-medium uppercase tracking-[0.18em] text-teal-700">
              Scrapbook Studio
            </div>
            <h1 className="mt-4 text-4xl font-semibold tracking-tight text-gray-900">Build visual memory boards from your photos and videos.</h1>
            <p className="mt-3 max-w-xl text-sm leading-6 text-gray-600">
              Start a new scrapbook, then drag media from your library onto a blank page and arrange everything the way you want.
            </p>
          </div>

          <button
            type="button"
            onClick={createNewScrapbook}
            className="inline-flex items-center justify-center gap-2 rounded-2xl bg-teal-500 px-5 py-3 text-sm font-medium text-white shadow-sm transition hover:bg-teal-600"
          >
            <Plus size={18} />
            Create New Scrapbook
          </button>
        </div>
      </section>

      <div className="mb-4 flex items-center justify-between">
        <div>
          <h2 className="text-xl font-semibold text-gray-900">Previous scrapbooks</h2>
          <p className="text-sm text-gray-500">Open an existing board or rename and delete older ones.</p>
        </div>
        <div className="rounded-full bg-white/90 px-4 py-2 text-sm text-gray-600 shadow-sm">
          {scrapbookCards.length} saved
        </div>
      </div>

      {scrapbookCards.length === 0 ? (
        <div className="rounded-[24px] border border-dashed border-teal-200 bg-white/90 p-10 text-center text-gray-500 shadow-sm">
          No scrapbooks yet. Create your first scrapbook to get started.
        </div>
      ) : (
        <div className="grid grid-cols-1 gap-4 md:grid-cols-2 xl:grid-cols-3">
          {scrapbookCards.map((scrapbook) => (
            <div
              key={scrapbook.id}
              onClick={() => editingId !== scrapbook.id && openScrapbook(scrapbook.id)}
              className="group relative cursor-pointer rounded-[24px] border border-white/70 bg-white/95 p-6 text-left shadow-sm transition hover:-translate-y-0.5 hover:shadow-md"
            >
              <div className="mb-4 flex items-center justify-between text-xs uppercase tracking-[0.18em] text-gray-400">
                <span>Scrapbook</span>
                <span>{scrapbook.itemCount} items</span>
              </div>

              {editingId === scrapbook.id ? (
                <div className="flex items-center gap-2 mb-2">
                  <input
                    type="text"
                    value={editingName}
                    onChange={(e) => setEditingName(e.target.value)}
                    onClick={(e) => e.stopPropagation()}
                    onKeyDown={(e) => {
                      if (e.key === 'Enter') confirmRename(e);
                      if (e.key === 'Escape') cancelRename(e);
                    }}
                    className="flex-1 px-2 py-1 border border-gray-300 rounded text-sm focus:outline-none focus:ring-1 focus:ring-teal-400"
                    autoFocus
                  />
                  <button onClick={confirmRename} className="text-green-600 hover:text-green-700" title="Confirm">
                    <Check size={16} />
                  </button>
                  <button onClick={cancelRename} className="text-gray-400 hover:text-gray-600" title="Cancel">
                    <X size={16} />
                  </button>
                </div>
              ) : (
                <div className="mb-4 flex items-start justify-between gap-3">
                  <div className="text-lg font-semibold text-gray-800">{scrapbook.name}</div>
                  <div className="flex items-center gap-1 opacity-0 group-hover:opacity-100 transition-opacity">
                    <button
                      onClick={(e) => startRename(e, scrapbook)}
                      className="p-1 rounded hover:bg-gray-100 text-gray-400 hover:text-teal-500"
                      title="Rename"
                    >
                      <Pencil size={14} />
                    </button>
                    <button
                      onClick={(e) => deleteScrapbook(e, scrapbook.id)}
                      className="p-1 rounded hover:bg-gray-100 text-gray-400 hover:text-red-500"
                      title="Delete"
                    >
                      <Trash2 size={14} />
                    </button>
                  </div>
                </div>
              )}

              <div className="rounded-2xl bg-gradient-to-br from-teal-50 to-sky-50 px-4 py-4">
                <div className="text-xs font-medium uppercase tracking-[0.18em] text-teal-700">Last edited</div>
                <div className="mt-1 text-sm text-gray-600">
                  {new Date(scrapbook.updatedAt || scrapbook.createdAt).toLocaleString()}
                </div>
                <div className="mt-4 inline-flex items-center gap-2 text-sm font-medium text-teal-700">
                  Open scrapbook
                  <ArrowRight size={16} />
                </div>
              </div>
            </div>
          ))}
        </div>
      )}
    </div>
  );
}

export default ScrapbookPage;
