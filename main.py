from television import Television  # import statement needed to gain access to Television class

def main():
    tv = Television()
    while True:
      tv.update()

if __name__ == '__main__':
    main()
