--
-- Copyright: 2013, Technical University of Denmark, DTU Compute
-- Author: Martin Schoeberl (martin@jopdesign.com)
-- License: Simplified BSD License
--

-- Hardware Hello World with Chisel - VHDL top level

library ieee;
use ieee.std_logic_1164.all;
use ieee.numeric_std.all;

entity fsm_top is
	port(
		clk : in  std_logic;
		--		rst : in std_logic;
		led : out std_logic_vector(7 downto 0)
	);
end entity fsm_top;

architecture rtl of fsm_top is

component FsmContainer is port (
	clk : in std_logic;
	reset : in std_logic;
    io_led : out std_logic_vector(7 downto 0)
);
end component;

begin

	comp: FsmContainer port map (
		clk, '0', led
	);
	
end architecture rtl;
