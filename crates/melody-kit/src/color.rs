use rand::{thread_rng, Rng};

use crate::types::Color;

/// MelodyKit's purple color (`#CC55FF`).
pub const MELODY_PURPLE: Color = 0xCC55FF;

/// MelodyKit's blue color (`#55CCFF`).
pub const MELODY_BLUE: Color = 0x55CCFF;

pub fn choose() -> Color {
    if thread_rng().gen_bool(0.5) {
        MELODY_PURPLE
    } else {
        MELODY_BLUE
    }
}
