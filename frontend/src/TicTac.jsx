import React, { useEffect, useState } from "react";

const initialBoard = Array(9).fill(null);

function TucTac() {
  const [board, setBoard] = useState(initialBoard);
  const [isUserTurn, setIsUserTurn] = useState(true);
  const [winner, setWinner] = useState(null);
  const [scores, setScores] = useState({ user: 0, cpu: 0, draw: 0 });

  // ✅ Load from localStorage
  useEffect(() => {
    const savedBoard = JSON.parse(localStorage.getItem("tuctac_board"));
    const savedScores = JSON.parse(localStorage.getItem("tuctac_scores"));

    if (savedBoard) setBoard(savedBoard);
    if (savedScores) setScores(savedScores);
  }, []);

  useEffect(() => {
    localStorage.setItem("tuctac_board", JSON.stringify(board));
  }, [board]);

  useEffect(() => {
    localStorage.setItem("tuctac_scores", JSON.stringify(scores));
  }, [scores]);

  // Check winner
  const checkWinner = (b) => {
    const lines = [
      [0, 1, 2],
      [3, 4, 5],
      [6, 7, 8],
      [0, 3, 6],
      [1, 4, 7],
      [2, 5, 8],
      [0, 4, 8],
      [2, 4, 6],
    ];
    for (let [a, bIdx, c] of lines) {
      if (b[a] && b[a] === b[bIdx] && b[a] === b[c]) {
        return b[a];
      }
    }
    return b.every((cell) => cell) ? "draw" : null;
  };

  // Handle user move
  const handleClick = (index) => {
    if (board[index] || winner || !isUserTurn) return;

    const newBoard = [...board];
    newBoard[index] = "X"; // ✅ user move
    setBoard(newBoard);
    setIsUserTurn(false);

    const result = checkWinner(newBoard);
    if (result) {
      endGame(result);
    } else {
      setTimeout(() => cpuMove(newBoard), 500);
    }
  };

  // ✅ Minimax AI
  const minimax = (b, depth, isMaximizing) => {
    const result = checkWinner(b);
    if (result === "X") return -10 + depth;
    if (result === "O") return 10 - depth;
    if (result === "draw") return 0;

    if (isMaximizing) {
      let best = -Infinity;
      for (let i = 0; i < 9; i++) {
        if (!b[i]) {
          b[i] = "O";
          best = Math.max(best, minimax(b, depth + 1, false));
          b[i] = null;
        }
      }
      return best;
    } else {
      let best = Infinity;
      for (let i = 0; i < 9; i++) {
        if (!b[i]) {
          b[i] = "X";
          best = Math.min(best, minimax(b, depth + 1, true));
          b[i] = null;
        }
      }
      return best;
    }
  };

  // CPU move using minimax
  const cpuMove = (currentBoard) => {
    let bestScore = -Infinity;
    let move = null;

    for (let i = 0; i < 9; i++) {
      if (!currentBoard[i]) {
        currentBoard[i] = "O";
        let score = minimax(currentBoard, 0, false);
        currentBoard[i] = null;
        if (score > bestScore) {
          bestScore = score;
          move = i;
        }
      }
    }

    if (move !== null) {
      const newBoard = [...currentBoard];
      newBoard[move] = "O";
      setBoard(newBoard);

      const result = checkWinner(newBoard);
      if (result) {
        endGame(result);
      } else {
        setIsUserTurn(true);
      }
    }
  };

  // End game
  const endGame = (result) => {
    setWinner(result);
    if (result === "X") {
      setScores((s) => ({ ...s, user: s.user + 1 }));
    } else if (result === "O") {
      setScores((s) => ({ ...s, cpu: s.cpu + 1 }));
    } else if (result === "draw") {
      setScores((s) => ({ ...s, draw: s.draw + 1 }));
    }
  };

  // Retry → reset only board
  const retry = () => {
    setBoard(initialBoard);
    setWinner(null);
    setIsUserTurn(true);
    localStorage.removeItem("tuctac_board");
  };

  // Reset all
  const resetScores = () => {
    setScores({ user: 0, cpu: 0, draw: 0 });
    retry();
    localStorage.removeItem("tuctac_scores");
  };

  return (
    <div className="flex flex-col items-center justify-center min-h-screen text-white">
        <p className="text-lg text-zinc-200 animate-pulse">
        🌍 Fetching vibes... this may take up to 2 minutes..till then, enjoy a game of Tic Tac Toe!
        </p>
      <h1 className="text-3xl font-bold mb-4">🎮 Tic Tac Toe</h1>

      {/* Scoreboard */}
      <div className="mb-6 bg-black/30 p-4 rounded-lg shadow-md text-center">
        <p>🙂 You: {scores.user}</p>
        <p>🤖 CPU: {scores.cpu}</p>
        <p>😐 Draws: {scores.draw}</p>
      </div>

      {/* Board */}
      <div className="grid grid-cols-3 gap-2 mb-4">
        {board.map((cell, i) => (
          <button
            key={i}
            onClick={() => handleClick(i)}
            className="w-20 h-20 flex items-center justify-center text-3xl font-bold bg-black/40 rounded-lg hover:bg-black/60 transition"
          >
            {cell}
          </button>
        ))}
      </div>

      {/* Status */}
      {winner ? (
        <div className="text-center">
          <p className="text-xl font-bold mb-2">
            {winner === "draw"
              ? "😐 It's a Draw!"
              : winner === "X"
              ? "🎉 You Win!"
              : "💀 CPU Wins!"}
          </p>
          <button
            onClick={retry}
            className="px-4 py-2 bg-green-600 rounded-lg hover:bg-green-500 mr-2"
          >
            Retry
          </button>
          <button
            onClick={resetScores}
            className="px-4 py-2 bg-red-600 rounded-lg hover:bg-red-500"
          >
            Reset Scores
          </button>
        </div>
      ) : (
        <p className="text-sm italic text-zinc-400">
          {isUserTurn ? "Your turn 🙂" : "CPU is thinking... 🤖"}
        </p>
      )}
    </div>
  );
}

export default TucTac;
