--
-- Copyright: 2013, Technical University of Denmark, DTU Compute
-- Author: Martin Schoeberl (martin@jopdesign.com)
-- License: Simplified BSD License
--

-- Hardware Hello World

library ieee;
use ieee.std_logic_1164.all;
use ieee.numeric_std.all;

entity blink is
	port(
		clk : in  std_logic;
		--		rst : in std_logic;
		led : out std_logic
	);
end entity blink;

architecture rtl of blink is

    constant CLK_FREQ : integer := 16000000; -- 16 MHz
    constant BLINK_FREQ : integer := 1; -- 1 Hz
    constant CNT_MAX : integer := CLK_FREQ/BLINK_FREQ/2-1;

	signal cnt : unsigned(24 downto 0);
	signal blk : std_logic;

begin
	process(clk)
	begin
		if rising_edge(clk) then
			if cnt = CNT_MAX then
				cnt <= (others => '0');
				blk <= not blk;
			else
				cnt <= cnt + 1;
			end if;
		end if;

	end process;

	led <= blk;
	
end architecture rtl;
