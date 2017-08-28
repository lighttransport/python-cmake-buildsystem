# Sanity checks
foreach(varname INPUT_DEF_FILE OUTPUT_DEF_FILE)
  if(NOT DEFINED ${varname})
    message(FATAL_ERROR "Variable '${varname}' is not defined.")
  endif()
endforeach()

# read in strings with "="
file(STRINGS ${INPUT_DEF_FILE} def_lines REGEX ".*=.*")

# initialize output file
file(WRITE ${OUTPUT_DEF_FILE} "EXPORTS")

# run through each line
foreach(line IN LISTS def_lines)

  # kill "=..." in the line
  string(REGEX REPLACE "=.+" "" updated_line ${line})

  # stick on end of file
  file(APPEND ${OUTPUT_DEF_FILE} "${updated_line}\n")

endforeach(line IN def_lines)
