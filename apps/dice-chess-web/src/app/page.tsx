import Link from 'next/link';

export default function Home() {
  return (
    <main className="landing-hero">
      <h1 className="landing-title">
        <span className="highlight">Dice</span> Chess
      </h1>
      <p className="landing-subtitle">
        A unique twist on chess — roll the dice to determine which piece you can move.
        Strategy meets chance in every turn!
      </p>

      <div className="landing-buttons">
        <Link href="/play/local" className="landing-btn local" id="play-local-btn">
          👥 Play Local
        </Link>
        <Link href="/play/ai" className="landing-btn ai" id="play-ai-btn">
          🤖 Play vs AI
        </Link>
        <Link href="/play/online" className="landing-btn online" id="play-online-btn">
          🌐 Play Online
        </Link>
      </div>

      <section className="rules-section">
        <div className="rules-card">
          <h2 className="rules-title">How to Play</h2>
          <ul className="rules-list">
            <li>
              <span className="rules-icon">1</span>
              <span>Standard chess rules apply — same pieces, same movements, same objective.</span>
            </li>
            <li>
              <span className="rules-icon">2</span>
              <span>Before each move, you <strong>roll a dice</strong>. The dice randomly selects a piece type.</span>
            </li>
            <li>
              <span className="rules-icon">3</span>
              <span>You can only move a piece of the <strong>rolled type</strong>. Pieces with valid moves are highlighted.</span>
            </li>
            <li>
              <span className="rules-icon">4</span>
              <span>The dice only shows piece types that <strong>have legal moves</strong>, so you&apos;re never stuck.</span>
            </li>
            <li>
              <span className="rules-icon">5</span>
              <span>All special moves — castling, en passant, promotion — work as normal!</span>
            </li>
            <li>
              <span className="rules-icon">🏆</span>
              <span>Win by checkmate, or draw by stalemate. Strategy + luck = Dice Chess!</span>
            </li>
          </ul>
        </div>
      </section>
    </main>
  );
}
