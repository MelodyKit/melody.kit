(trap "kill 0" SIGINT; cargo run --release kit & cargo run --release web & cargo run --release bot & wait)
