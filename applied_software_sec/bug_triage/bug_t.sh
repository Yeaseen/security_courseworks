for crash_file in out/default/crashes/*; do
  echo "Testing file: $crash_file"
  ./fuzzgoat_ASAN "$crash_file" 2>&1 | grep "SUMMARY"
done
