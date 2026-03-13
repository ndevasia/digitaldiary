import { useState } from 'react';

function SetupPage() {
    const [username, setUsername] = useState('');
    const [error, setError] = useState('');

    const handleSubmit = (event) => {
        event.preventDefault();
        const cleanUsername = username.trim();

        if (!cleanUsername) {
            setError('Please enter a username to continue.');
            return;
        }

        localStorage.setItem('username', cleanUsername);
        window.location.reload();
    };

    return (
        <div className="relative min-h-screen w-full overflow-hidden bg-gradient-to-br from-cyan-50 via-white to-teal-100 p-6">
            <div className="pointer-events-none absolute -left-20 top-10 h-60 w-60 rounded-full bg-cyan-200/50 blur-3xl" />
            <div className="pointer-events-none absolute -bottom-24 right-0 h-72 w-72 rounded-full bg-emerald-200/60 blur-3xl" />

            <div className="mx-auto flex min-h-[calc(100vh-3rem)] w-full max-w-4xl items-center justify-center">
                <div className="w-full max-w-xl rounded-3xl border border-white/70 bg-white/90 p-8 text-center shadow-[0_18px_60px_-20px_rgba(15,23,42,0.35)] backdrop-blur-xl sm:p-10">
                    <p className="mb-4 inline-flex rounded-full bg-teal-100 px-4 py-1 text-xs font-semibold tracking-[0.2em] text-teal-700 uppercase">
                        Welcome
                    </p>

                    <h1 className="text-4xl font-black tracking-tight text-slate-900 sm:text-5xl">
                        Digital Diary
                    </h1>

                    <p className="mx-auto mt-4 max-w-md text-base leading-relaxed text-slate-600 sm:text-lg">
                        Give your timeline a name so we can personalize your memories and activity feed.
                    </p>

                    <form onSubmit={handleSubmit} className="mt-8 space-y-4">
                        <label htmlFor="username" className="sr-only">Username</label>
                        <input
                            id="username"
                            type="text"
                            value={username}
                            onChange={(event) => {
                                setUsername(event.target.value);
                                if (error) {
                                    setError('');
                                }
                            }}
                            placeholder="Enter your username"
                            className="w-full rounded-2xl border border-slate-200 bg-white px-5 py-4 text-center text-lg font-medium text-slate-700 shadow-inner outline-none transition focus:border-teal-400 focus:ring-4 focus:ring-teal-100"
                            autoFocus
                        />

                        {error && (
                            <p className="text-sm font-medium text-rose-600">{error}</p>
                        )}

                        <button
                            type="submit"
                            className="w-full rounded-2xl bg-gradient-to-r from-teal-500 to-cyan-500 px-5 py-4 text-base font-bold text-white shadow-lg shadow-cyan-200/70 transition hover:from-teal-600 hover:to-cyan-600"
                        >
                            Continue
                        </button>
                    </form>
                </div>
            </div>
        </div>
    );
}

export default SetupPage;