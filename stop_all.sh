#!/bin/bash
set -euo pipefail

SCRIPT_DIR="$(cd "$(dirname "$0")" && pwd)"
PID_DIR="$SCRIPT_DIR/.pids"

# Ensure PID dir exists
mkdir -p "$PID_DIR"

echo "Stopping project servers (safe mode)..."

# Helpers and safety checks
CURRENT_PID=$$
PARENT_PID=$PPID
CURRENT_USER=$(whoami 2>/dev/null || echo "$USER")

# Kill process whose PID is stored in a file, with graceful then force kill
kill_pidfile() {
  local f="$1"
  if [ -f "$f" ]; then
    local pid
    pid=$(cat "$f" 2>/dev/null || true)
    if [ -n "$pid" ] && kill -0 "$pid" 2>/dev/null; then
      # don't kill ourselves or parent
      if [ "$pid" -eq "$CURRENT_PID" ] || [ "$pid" -eq "$PARENT_PID" ]; then
        echo "Skipping PID $pid (self/parent) from $f"
      else
        echo "Stopping PID $pid from $f"
        kill "$pid" 2>/dev/null || true
        sleep 1
        if kill -0 "$pid" 2>/dev/null; then
          echo "PID $pid still alive; forcing"
          kill -9 "$pid" 2>/dev/null || true
        fi
      fi
    else
      echo "No running process for PID file $f"
    fi
    rm -f "$f"
  fi
}

kill_pidfile "$PID_DIR/backend.pid"
kill_pidfile "$PID_DIR/frontend.pid"

# Fallback: kill processes listening on known ports (8000 backend, 5173 frontend)
kill_by_port() {
  local port="$1"
  local pids
  # lsof may not be present on all systems; ignore failures
  pids=$(lsof -t -i:"$port" 2>/dev/null || true)
  if [ -n "$pids" ]; then
    for p in $pids; do
      # skip current shell and parent
      if [ "$p" -eq "$CURRENT_PID" ] || [ "$p" -eq "$PARENT_PID" ]; then
        echo "Skipping local shell PID $p for port $port"
        continue
      fi
      # only kill processes owned by current user
      owner=$(ps -o user= -p $p 2>/dev/null || true)
      if [ -n "$owner" ] && [ "$owner" != "$CURRENT_USER" ]; then
        echo "Skipping PID $p owned by $owner (not $CURRENT_USER)"
        continue
      fi
      echo "Stopping process $p listening on port $port"
      kill $p 2>/dev/null || true
      sleep 1
      if kill -0 $p 2>/dev/null; then
        echo "Force killing $p"
        kill -9 $p 2>/dev/null || true
      fi
    done
  else
    echo "No processes listening on port $port"
  fi
}

kill_by_port 8000 || true
kill_by_port 5173 || true

# Last-resort: patterns commonly used for these dev servers
# We filter matches to the current user and avoid killing the current shell or its parent
for pattern in "manage.py runserver" "python manage.py" "npm run dev" "vite" "node"; do
  pids=$(pgrep -f "$pattern" || true)
  if [ -n "$pids" ]; then
    for p in $pids; do
      if [ "$p" -eq "$CURRENT_PID" ] || [ "$p" -eq "$PARENT_PID" ]; then
        echo "Skipping PID $p (self/parent) matching '$pattern'"
        continue
      fi
      owner=$(ps -o user= -p $p 2>/dev/null || true)
      if [ -n "$owner" ] && [ "$owner" != "$CURRENT_USER" ]; then
        echo "Skipping PID $p owned by $owner (pattern: $pattern)"
        continue
      fi
      # Extra safety: only kill commands that clearly include our project path
      cmdline=$(tr '\0' ' ' < /proc/$p/cmdline 2>/dev/null || true)
      if [ -n "$cmdline" ] && echo "$cmdline" | grep -q "${SCRIPT_DIR}"; then
        echo "Stopping PID $p matching '$pattern' (cmd: $cmdline)"
        kill $p 2>/dev/null || true
        sleep 1
        if kill -0 $p 2>/dev/null; then
          echo "Force killing $p"
          kill -9 $p 2>/dev/null || true
        fi
      else
        echo "Skipping PID $p because cmdline does not contain project dir"
      fi
    done
  fi
done

# Clean up any empty PID files
if [ -d "$PID_DIR" ]; then
  find "$PID_DIR" -type f -empty -delete || true
fi

echo "Done stopping servers."
