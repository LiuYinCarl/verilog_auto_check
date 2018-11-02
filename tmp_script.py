for i in ['always', 'and', 'assign', 'wor', 'xor',
          'automatic', 'begin', 'case', 'casex', 'casez',
          'cell', 'deassign', 'default', 'defparam', 'design',
          'disable', 'edge', 'else', 'end', 'endcase',
          'endconfig', 'endfunction', 'endgenerate', 'endmodule', 'endprimitive',
          'endtable', 'endtask', 'event', 'for', 'force',
          'forever', 'fork', 'function', 'inout', 'input',
          'integer', 'reg', 'wire', 'while', 'xnor',
          ]:
    print('text = re.sub(\'{}\', \'{}\', text, flags=re.IGNORECASE)'.format(i, i))
