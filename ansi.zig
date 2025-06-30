const ANSI = struct {
    sequence: []const u8,
    no_of_arguments: u8,
    no_of_default_arguments: u8
};

pub const CSI = "\x1b[";

pub const AUX_PORT_OFF = ANSI {
	.sequence = "4i",
	.no_of_arguments = 0,
	.no_of_default_arguments = 0,
};

pub const AUX_PORT_ON = ANSI {
	.sequence = "5i",
	.no_of_arguments = 0,
	.no_of_default_arguments = 0,
};

pub const CURSOR_BACK = ANSI {
	.sequence = "D",
	.no_of_arguments = 1,
	.no_of_default_arguments = 1,
};

pub const CURSOR_DOWN = ANSI {
	.sequence = "B",
	.no_of_arguments = 1,
	.no_of_default_arguments = 1,
};

pub const CURSOR_FORWARD = ANSI {
	.sequence = "C",
	.no_of_arguments = 1,
	.no_of_default_arguments = 1,
};

pub const CURSOR_HORIZONTAL_ABSOLUTE = ANSI {
	.sequence = "G",
	.no_of_arguments = 1,
	.no_of_default_arguments = 1,
};

pub const CURSOR_NEXT_LINE = ANSI {
	.sequence = "E",
	.no_of_arguments = 1,
	.no_of_default_arguments = 1,
};

pub const CURSOR_POSITION = ANSI {
	.sequence = "H",
	.no_of_arguments = 2,
	.no_of_default_arguments = 0,
};

pub const CURSOR_PREVIOUS_LINE = ANSI {
	.sequence = "F",
	.no_of_arguments = 1,
	.no_of_default_arguments = 1,
};

pub const CURSOR_UP = ANSI {
	.sequence = "A",
	.no_of_arguments = 1,
	.no_of_default_arguments = 1,
};

pub const DEVICE_STATUS_REPORT = ANSI {
	.sequence = "6n",
	.no_of_arguments = 0,
	.no_of_default_arguments = 0,
};

pub const ERASE_IN_DISPLAY = ANSI {
	.sequence = "J",
	.no_of_arguments = 1,
	.no_of_default_arguments = 1,
};

pub const ERASE_IN_LINE = ANSI {
	.sequence = "K",
	.no_of_arguments = 1,
	.no_of_default_arguments = 1,
};

pub const HIDE_CURSOR = ANSI {
	.sequence = "?25l",
	.no_of_arguments = 0,
	.no_of_default_arguments = 0,
};

pub const HORIZONTAL_VERTICAL_POSITION = ANSI {
	.sequence = "f",
	.no_of_arguments = 2,
	.no_of_default_arguments = 0,
};

pub const INSERT_NEW_LINE = ANSI {
	.sequence = "L",
	.no_of_arguments = 0,
	.no_of_default_arguments = 0,
};

pub const REMOVE_CHARACTER = ANSI {
	.sequence = "P",
	.no_of_arguments = 0,
	.no_of_default_arguments = 0,
};

pub const REMOVE_LINE = ANSI {
	.sequence = "M",
	.no_of_arguments = 0,
	.no_of_default_arguments = 0,
};

pub const RESTORE_SAVED_CURRENT_CURSOR_POSITION = ANSI {
	.sequence = "u",
	.no_of_arguments = 0,
	.no_of_default_arguments = 0,
};

pub const SAVE_CURRENT_CURSOR_POSITION = ANSI {
	.sequence = "s",
	.no_of_arguments = 0,
	.no_of_default_arguments = 0,
};

pub const SCROLL_DOWN = ANSI {
	.sequence = "S",
	.no_of_arguments = 1,
	.no_of_default_arguments = 1,
};

pub const SCROLL_UP = ANSI {
	.sequence = "T",
	.no_of_arguments = 1,
	.no_of_default_arguments = 1,
};

pub const SELECT_CHARACTER_RENDITION = ANSI {
	.sequence = "m",
	.no_of_arguments = 3,
	.no_of_default_arguments = 3,
};

pub const SHOW_CURSOR = ANSI {
	.sequence = "?25h",
	.no_of_arguments = 0,
	.no_of_default_arguments = 0,
};

pub const BACKGROND_BLACK = 40;

pub const BACKGROND_BLUE = 44;

pub const BACKGROND_CYAN = 46;

pub const BACKGROND_DEFAULT = 48;

pub const BACKGROND_GREEN = 42;

pub const BACKGROND_MAGENTA = 45;

pub const BACKGROND_RED = 41;

pub const BACKGROND_WHITE = 47;

pub const BACKGROND_YELLOW = 43;

pub const ERASE_IN_DISPLAY_ALL = 2;

pub const ERASE_IN_DISPLAY_TO_BEGINNING = 1;

pub const ERASE_IN_DISPLAY_TO_END = 0;

pub const ERASE_IN_LINE_ALL = 2;

pub const ERASE_IN_LINE_BEGINNING = 1;

pub const ERASE_IN_LINE_END = 0;

pub const FOREGROND_BLACK = 30;

pub const FOREGROND_BLUE = 34;

pub const FOREGROND_CYAN = 36;

pub const FOREGROND_DEFAULT = 38;

pub const FOREGROND_GREEN = 32;

pub const FOREGROND_MAGENTA = 35;

pub const FOREGROND_RED = 31;

pub const FOREGROND_WHITE = 37;

pub const FOREGROND_YELLOW = 33;

pub const SCR_RESET = 0;

pub const SET_BLINKING_MODE = 5;

pub const SET_BOLD_MODE = 1;

pub const SET_DIM_MODE = 2;

pub const SET_INVERSE_MODE = 7;

pub const SET_INVISIBLE_MODE = 8;

pub const SET_ITALIC_MODE = 3;

pub const SET_STRIKETHROUGH_MODE = 9;

pub const SET_UNDERLINE_MODE = 4;
