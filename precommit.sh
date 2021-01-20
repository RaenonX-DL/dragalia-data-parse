# ------ Variables

CLR_RED=[31m
CLR_GRN=[32m
CLR_CYN=[36m
CLR_NC=[0m

# ------ Functions

run_cmd_exit_on_err() {
  if ! $1; then
    echo "${CLR_RED}Error @ $2${CLR_NC}"
    read -p "Press enter to continue." -r
    exit 1
  fi
}

# ------ Code linting

echo "${CLR_CYN}Checking with pydocstyle (dlparse)...${CLR_NC}"
run_cmd_exit_on_err "pydocstyle dlparse --count" "pydocstyle check (dlparse)"

echo "${CLR_CYN}Checking with flake8 (dlparse)...${CLR_NC}"
run_cmd_exit_on_err "flake8 dlparse --count" "flake8 check (dlparse)"

echo "${CLR_CYN}Checking with bandit (dlparse)...${CLR_NC}"
run_cmd_exit_on_err "bandit -r dlparse" "bandit check (dlparse)"

echo "${CLR_CYN}Checking with pylint (dlparse)...${CLR_NC}"
run_cmd_exit_on_err "pylint dlparse" "pylint check (dlparse)"

echo "${CLR_CYN}Checking with pydocstyle (tests.utils)...${CLR_NC}"
run_cmd_exit_on_err "pydocstyle tests.utils --count" "pydocstyle check (tests.utils)"

echo "${CLR_CYN}Checking with flake8 (tests.utils)...${CLR_NC}"
run_cmd_exit_on_err "flake8 tests/utils --count" "flake8 check (tests.utils)"

echo "${CLR_CYN}Checking with bandit (tests.utils)...${CLR_NC}"
run_cmd_exit_on_err "bandit -r tests/utils" "bandit check (tests.utils)"

echo "${CLR_CYN}Checking with pylint (tests.utils)...${CLR_NC}"
run_cmd_exit_on_err "pylint tests.utils" "pylint check (tests.utils)"

echo "${CLR_CYN}Running code tests...${CLR_NC}"
run_cmd_exit_on_err "pytest --slow" "code test"

echo "--- ${CLR_GRN}All checks passed.${CLR_NC} ---"
read -p "Press enter to continue." -r
