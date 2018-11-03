module ji_shu(clk_1hz, time0, time1, time2, time3);

	input clk_1hz;
	output time0;
	output time1;
	output time2;
	output time3;
	
	reg[3:0] count1;
	reg[7:0] count2;
	reg[11:0] count3;
	
	
	reg[3:0] time0;
	reg[3:0] time1;
	reg[3:0] time2;
	reg[3:0] time3;
	
	always@(posedge clk_1hz)
	begin
		if(time0 == 9)
			time0 = 0;
		else time0 = time0 + 1;
	end
	
	always@(posedge clk_1hz)
	begin
		if(count1 == 9)
		begin
			count1 = 0;//÷√Œª
			if(time1 == 5)
				time1 = 0;
			else time1 = time1 + 1;
		end
		else count1 = count1 + 1;
	end
	
	always@(posedge clk_1hz)
	begin
		if(count2 == 59)
		begin
		count2 = 0;//÷√Œª
			if(time2 == 9)
				time2 = 0;
			else time2 = time2 + 1;
		end
		else count2 = count2 + 1;
	end
	
	always@(posedge clk_1hz)
	begin
		if(count3 == 599)
		begin
			count3 = 0;//÷√Œª
			if(time3 == 2)
				time3 = 0;
			else time3 = time3 + 1;
		end
		else count3 = count3 + 1;
	end
endmodule