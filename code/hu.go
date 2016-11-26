package main

import (
	"bufio"
	"encoding/json"
	"fmt"
	"io"
	"os"
	"sort"
)

func getPaiCount(pai []int) map[int]int {
	paiCount := make(map[int]int, 0)
	for _, j := range pai {
		_, ok := paiCount[j]
		if ok {
			paiCount[j] = paiCount[j] + 1
		} else {
			paiCount[j] = 1
		}
	}
	return paiCount
}

func hasGuzhang(pai []int, paiCount map[int]int) bool {
	for _, j := range pai {
		if paiCount[j] == 1 && paiCount[j+1] == 0 && paiCount[j-1] == 0 {
			return true
		}
	}
	return false
}

func findDuiPos(pai []int) []int {
	pos := []int{}
	for i := 0; i < len(pai)-1; i++ {
		if pai[i] == pai[i+1] {
			pos = append(pos, i)
			i++
		}
	}
	return pos
}

func removeDui(pai []int, duiPos int) []int {
	tmp := make([]int, 0)
	tmp = append(tmp, pai[:duiPos]...)
	tmp = append(tmp, pai[duiPos+2:]...)
	return tmp
}

func findAndRemoveKe(pai *[]int) bool {
	v := *pai
	if v[0] == v[1] && v[1] == v[2] {
		tmp := make([]int, 0)
		tmp = append(tmp, v[3:]...)
		*pai = tmp
		return true
	}
	return false
}

func findAndRemoveShun(pai *[]int) bool {
	v := *pai
	tmp := make([]int, 0)
	for i := 1; i < len(v); i++ {
		switch {
		case v[i] == v[i-1]:
			tmp = append(tmp, v[i])
		case v[i] == v[i-1]+1:
			if v[i]-v[0] == 2 {
				tmp = append(tmp, v[i+1:]...)
				*pai = tmp
				return true
			}
		default:
			return false
		}
	}
	return false
}

func findAndRemoveKeOrShun(pai *[]int) bool {
	find := findAndRemoveKe(pai)
	if find {
		return true
	} else {
		return findAndRemoveShun(pai)
	}
}

func AllIsShunOrKe(pai []int) bool {
	// 不断从头到尾遍历，先找刻字，在找顺子(如果是刻字一定是刻字，不需要在组合为顺子 -- 陈虎发现)
	count := len(pai)
	for i := 0; i < count/3; i++ {
		find := findAndRemoveKeOrShun(&pai)
		if !find {
			return false
		}
	}
	return len(pai) == 0
}

func hu(pai []int) bool {
	sort.Ints(pai)
	paiCount := getPaiCount(pai)
	if hasGuzhang(pai, paiCount) {
		return false
	}
	pos := findDuiPos(pai)
	if len(pos) == 7 {
		return true
	}
	for _, v := range pos {
		tmp := removeDui(pai, v)
		if AllIsShunOrKe(tmp) {
			return true
		}
	}
	return false
}

func main() {
	//beginTest()
	//pai := []int{7, 9, 9, 8, 1, 1, 1, 2, 2, 3, 3, 4, 4, 6}
	pai := []int{21, 21, 21, 22, 22, 22, 23, 23, 23, 24, 24, 24, 25, 25}
	//7 9 9 8 1 1 1 2 2 3 3 4 4 6
	fmt.Println(hu(pai))
}

func beginTest() []t {
	name := "right"
	f, err := os.Open(name)
	if err != nil {
		panic("open file filed")
	}
	defer f.Close()
	r := bufio.NewReader(f)
	count := 0
	for {
		var test t
		line, _, err := r.ReadLine()
		if err == io.EOF {
			break
		}
		json.Unmarshal(line, &test)
		if hu(test.Pai) == test.Expect {
			fmt.Println("test case success", count)
			count++
		} else {
			fmt.Println(test.Pai, test.Expect)
			panic("not expect")
		}
	}
	return []t{}
}

type t struct {
	Pai    []int
	Expect bool
}
