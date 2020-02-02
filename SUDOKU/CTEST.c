#include <stdio.h>
#include <stdlib.h>

void getNextPermutation(int *p);
void line_print(int *p);
void line_set  (int *p, int n0, int n1, int n2, int n3, int n4, int n5, int n6, int n7, int n8);
int  line_comp (int *p, int n0, int n1, int n2, int n3, int n4, int n5, int n6, int n7, int n8);
int  check     (int *p0, int *p1, int *p2, int *p3, int *p4, int *p5, int *p6, int *p7, int *p8); 

int main() {
  int i;
  int count = 0;
  int count_max = -1;

  int p0[9] = {3,1,4,5,8,7,2,9,6};
  int p1[9] = {5,7,2,4,9,6,8,3,1};
  int p2[9] = {6,8,9,2,3,1,7,4,5};
  int p3[9] = {4,9,3,6,2,8,1,5,7};
  int p4[9] = {7,2,1,3,5,9,4,6,8};
  int p5[9] = {8,6,5,1,7,4,9,2,3};
  int p6[9] = {1,3,6,7,4,2,5,8,9};
  int p7[9] = {2,5,8,9,1,3,6,7,4};
  int p8[9] = {9,4,7,8,6,5,3,1,2};

//int p0[9] = {1,2,3,4,5,6,7,8,9};
//int p1[9] = {1,2,3,4,5,6,7,8,9};
//int p2[9] = {1,2,3,4,5,6,7,8,9};
//int p3[9] = {1,2,3,4,5,6,7,8,9};
//int p4[9] = {1,2,3,4,5,6,7,8,9};
//int p5[9] = {1,2,3,4,5,6,7,8,9};
//int p6[9] = {1,2,3,4,5,6,7,8,9};
//int p7[9] = {1,2,3,4,5,6,7,8,9};
//int p8[9] = {1,2,3,4,5,6,7,8,9};

  while(1) { // p0
    while(1) { // p1
      while(1) { // p2
        while(1) { // p3
          while(1) { // p4
            while(1) { // p5
              while(1) { // p6
                while(1) { // p7
                  while(1) { // p8
                    count ++;
                    if (count <= 10) {
                      printf("+++++ %d\n", count);
                      line_print(p0);
                      line_print(p1);
                      line_print(p2);
                      line_print(p3);
                      line_print(p4);
                      line_print(p5);
                      line_print(p6);
                      line_print(p7);
                      line_print(p8);
                    }
                    if (count == count_max) exit(0);

                    if (check(p0,p1,p2,p3,p4,p5,p6,p7,p8)) {
                      printf("ok7 (OK)\n");
                      if (count > 10) exit(0);
                    }
                    getNextPermutation(p8);
                    if (line_comp(p8,1,2,3,4,5,6,7,8,9)) break;
                  } // p8
                  getNextPermutation(p7);
                  if (line_comp(p7,1,2,3,4,5,6,7,8,9)) break;
                } // p7 
                getNextPermutation(p6);
                if (line_comp(p6,1,2,3,4,5,6,7,8,9)) break;
              } // p6 
              getNextPermutation(p5);
              if (line_comp(p5,1,2,3,4,5,6,7,8,9)) break;
            } // p5 
            getNextPermutation(p4);
            if (line_comp(p4,1,2,3,4,5,6,7,8,9)) break;
          } // p4 
          getNextPermutation(p3);
          if (line_comp(p3,1,2,3,4,5,6,7,8,9)) break;
        } // p3 
        getNextPermutation(p2);
        if (line_comp(p2,1,2,3,4,5,6,7,8,9)) break;
      } // p2 
      getNextPermutation(p1);
      if (line_comp(p1,1,2,3,4,5,6,7,8,9)) break;
    } // p1 
    getNextPermutation(p0);
    if (line_comp(p0,1,2,3,4,5,6,7,8,9)) exit(0);
  } // p0 

  return 0;
}

void getNextPermutation(int *p) {
  int i, j, k;
  int d_i[9];
  int d_x[9];
  int d_o[9];
  int isUpdate = 0;

  // pre MAIN (*p => d_i[])
  for (i=0; i<9; i++) {
    d_i[i] = *p;
    ++p;
  }

  // MAIN (d_i[] => d_o[])
  for (i=7; i>=0; i--) {
    if (d_i[i] < d_i[i+1]) {
      // generate new d_o[]
      for (j=8; j>i; j--) {
        if (d_i[i] < d_i[j]) {
          for (k=0; k<9; k++) {
            if (k == i)      d_x[k] = d_i[j];
            else if (k == j) d_x[k] = d_i[i];
            else             d_x[k] = d_i[k];
          }
          for (k=0; k<9; k++) {
            if (k <= i) d_o[k] = d_x[k];
            else        d_o[k] = d_x[8-(k-(i+1))];
          }
          isUpdate = 1;
          break;
        }
      }
      break;
    }
  }

  // 5 3 7   9 8 6 4 2 1    d_i[]
  //     i
  //           j
  // 5 3 8   9 7 6 4 2 1    d_x[]
  //
  // 5 3 8   1 2 4 6 7 9    d_o[]

  if (isUpdate == 0) {
    if (line_comp(d_i,9,8,7,6,5,4,3,2,1)) line_set(d_o,1,2,3,4,5,6,7,8,9);
    else {
      printf("Error\n");
      line_print(d_i);
      exit(0);
    }
  }

  // post MAIN (d_o[] => *p)
  p = p - 9;
  for (i=0; i<9; i++) {
    *p = d_o[i];
    ++p;
  }
}

void line_print(int *p) {
  int i;

  for (i=0; i<9; i++) {
    printf("%d", *p);
    ++p;
  }
  printf("\n");
}

void line_set(int *p, int n0, int n1, int n2, int n3, int n4, int n5, int n6, int n7, int n8) {
  *p = n0; ++p;
  *p = n1; ++p;
  *p = n2; ++p;
  *p = n3; ++p;
  *p = n4; ++p;
  *p = n5; ++p;
  *p = n6; ++p;
  *p = n7; ++p;
  *p = n8; ++p;
}

int line_comp(int *p, int n0, int n1, int n2, int n3, int n4, int n5, int n6, int n7, int n8) {
  int i;
  int flag = 1;

  if (*p != n0) flag = 0; ++p;
  if (*p != n1) flag = 0; ++p;
  if (*p != n2) flag = 0; ++p;
  if (*p != n3) flag = 0; ++p;
  if (*p != n4) flag = 0; ++p;
  if (*p != n5) flag = 0; ++p;
  if (*p != n6) flag = 0; ++p;
  if (*p != n7) flag = 0; ++p;
  if (*p != n8) flag = 0; ++p;
  return flag;    
}

int check(int *p0, int *p1, int *p2, int *p3, int *p4, int *p5, int *p6, int *p7, int *p8) {
  // ok return 1    ng return 0
  int i, i2, j, k, k2, kr, kc,kr2, kc2;
  int flag = 1;
  int d[9][9];

  for (j=0; j<9; j++) {
    d[0][j] = *p0; ++p0;    
    d[1][j] = *p1; ++p1;    
    d[2][j] = *p2; ++p2;    
    d[3][j] = *p3; ++p3;    
    d[4][j] = *p4; ++p4;    
    d[5][j] = *p5; ++p5;    
    d[6][j] = *p6; ++p6;    
    d[7][j] = *p7; ++p7;    
    d[8][j] = *p8; ++p8;    
  }

  for (j=0; j<9; j++) {
    for (i=0; i<9; i++) {
      for (i2=i+1; i2<9; i2++) {
        if (d[i][j] == d[i2][j]) return 0;
      }
    }
  }

  for (i=0; i<9; i=i+3) {
    for (j=0; j<9; j=j+3) {
      for (k=0; k<9; k++) {
        for (k2=k+1; k2<9; k2++) {
          kr = k / 3;
          kc = k % 3;
          kr2 = k2 / 3;
          kc2 = k2 % 3;
          if (d[kr][kc] == d[kr2][kc2]) return 0;
        }
      }
    }
  }

  return 1;
}
