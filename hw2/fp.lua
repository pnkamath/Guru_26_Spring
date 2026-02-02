-- C1
function collect(t, f)
  local out = {}
  for i, v in ipairs(t) do
    out[i] = f(v)
  end
  return out
end

-- C2
function select(t, f)
  local result = {}

  for _, v in ipairs(t) do
    if f(v) then
      table.insert(result, v)
    end
  end
  return result
end

-- C3
function reject(t, f)
  local out = {}
  for i, v in ipairs(t) do
    if not f(v) then
      table.insert(out, v)
    end
  end
  return out
end

-- C4
function inject(t, acc, f)
  for _, v in ipairs(t) do
    acc = f(acc, t[v])
  end

  return acc
end

-- C5
function detect(t, f)
  for i, v in ipairs(t) do
    if f(v) then return v end
  end
  return nil
end

-- C6
function range(start, stop, step)
  local current = start - step

  return function()
    current = current + step
    if current > stop then
      return nil
    end

    return current
  end
end

-- Test Helper function
function print_table(t)
  io.write("{")
  for i, v in ipairs(t) do
    io.write(v)
    if i < #t then
      io.write(", ")
    end
  end
  io.write("}\n")
end

-- Tests
-- C1 Test
print("C1 Test:")
local c1 = collect({1,2,3}, function(x) return x*x end)
-- print("C1:", table.concat(c1, ","))
print_table(c1)

-- C2 Test
print("C2 Test:")
local select_test = select({ 1, 2, 3, 4, 5 }, function(x) return x % 2 == 0 end)
print_table(select_test)

-- C3 Test
print("C3 Test:")
local c3 = reject({1,2,3,4,5}, function(x) return x%2==0 end)
print_table(c3)

-- C4 Tests
print("C4 Tests:")
local inject_test_1 = inject({ 1, 2, 3, 4 }, 0, function(a, x) return a + x end)
print(inject_test_1)

local inject_test_2 = inject({ 1, 2, 3, 4 }, 1, function(a, x) return a * x end)
print(inject_test_2)

-- C5 Test
print("C5 Test:")
local c5 = detect({1,2,3,4}, function(x) return x>2 end)
print(c5)

-- C6 Test
print("C6 Test:")
for x in range(1, 10, 2) do print(x) end
