/*
**	4-8转换器(共阴/共阳)
*/
module decode(in_4, bus_4, out_8);

	input[3:0] in_4;
	input[3:0] bus_4;
	output out_8;
	
	reg[7:0] out_8;
	
	/*
	//共阴版本
	always@(in_4)
		begin
			case(in_4)
			0 : out_8 = 8'h3f;
			1 : out_8 = 8'h06;
			2 : out_8 = 8'h5b;
			3 : out_8 = 8'h4f;
			4 : out_8 = 8'h66;
			5 : out_8 = 8'h6d;
			6 : out_8 = 8'h7d;
			7 : out_8 = 8'h07;
			8 : out_8 = 8'h7f;
			9 : out_8 = 8'h6f;
			10 : out_8 = 8'h77;
			11 : out_8 = 8'h7c;
			12 : out_8 = 8'h39;
			13 : out_8 = 8'h5e;
			14 : out_8 = 8'h79;
			15 : out_8 = 8'h71;
			default: out_8 = 8'h3f;	//出错显示0 
			endcase
		end
	*/	
		
	//共阳版本  
	always@(in_4)
		begin
			if(bus_4 == 4'b1101)
			begin
				case(in_4)
				0 : out_8 = 8'h40;
				1 : out_8 = 8'h79;
				2 : out_8 = 8'h24;
				3 : out_8 = 8'h30;
				4 : out_8 = 8'h19;
				5 : out_8 = 8'h12;
				6 : out_8 = 8'h02;
				7 : out_8 = 8'h78;
				8 : out_8 = 8'h00;
				9 : out_8 = 8'h10;
				10 : out_8 = 8'h08;
				11 : out_8 = 8'h03;
				12 : out_8 = 8'h46;
				13 : out_8 = 8'h21;
				14 : out_8 = 8'h06;
				15 : out_8 = 8'h0e;
				default: out_8 = 8'hc0;	//出错显示0 
				endcase
			end
			else
				begin
					case(in_4)
					0 : out_8 = 8'hc0;
					1 : out_8 = 8'hf9;
					2 : out_8 = 8'ha4;
					3 : out_8 = 8'hb0;
					4 : out_8 = 8'h99;
					5 : out_8 = 8'h92;
					6 : out_8 = 8'h82;
					7 : out_8 = 8'hf8;
					8 : out_8 = 8'h80;
					9 : out_8 = 8'h90;
					10 : out_8 = 8'h88;
					11 : out_8 = 8'h83;
					12 : out_8 = 8'hc6;
					13 : out_8 = 8'ha1;
					14 : out_8 = 8'h86;
					15 : out_8 = 8'h8e;
					default: out_8 = 8'hc0;	//出错显示0 
					endcase
				end
		end
endmodule