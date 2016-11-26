package sint

func Copy(s []int) []int {
	var slice = make([]int, len(s))
	copy(slice, s)
	return slice
}

func Contains(slice []int, finder ...int) bool {
	var j int
	for i := 0; i < len(finder); i++ {
		for j = 0; j < len(slice); j++ {
			if slice[j] == finder[i] {
				break
			}
		}
		if j == len(slice) {
			return false
		}
	}
	return true
}

func ToMap(slice []int) map[int]int {
	var m = map[int]int{}
	for _, j := range slice {
		var _, ok = m[j]
		if ok {
			m[j]++
		} else {
			m[j] = 1
		}
	}
	return m
}

func IsSame(slice1 []int, slice2 []int) bool {
	if len(slice1) != len(slice2) {
		return false
	}
	for i := 0; i < len(slice1); i++ {
		if slice1[i] != slice2[i] {
			return false
		}
	}
	return true
}

func Add(slice []int, values ...int) []int {
	return append(slice, values...)
}

func Del(slice []int, values ...int) []int {
	if slice == nil || len(values) == 0 {
		return slice
	}
	for _, value := range values {
		slice = sliceDel(slice, value)
	}
	return slice
}

func Update(slice []int, src, dst, count int) []int {
	var slice2 []int = Copy(slice)
	var flag = 0
	for i, v := range slice2 {
		if v == src {
			slice2[i] = dst
			flag++
		}
		if flag == count {
			break
		}
	}
	return slice2
}

func sliceDel(slice []int, value int) []int {
	if slice == nil {
		return slice
	}
	for i, j := range slice {
		if j == value {
			return append(slice[:i], slice[i+1:]...)
		}
	}
	return slice
}
