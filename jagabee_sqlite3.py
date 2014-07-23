# -*- coding: utf-8 -*-
import sys
import traceback
import getopt
import sqlite3

import sys
reload(sys)
sys.setdefaultencoding("utf-8")

'''
    table product:
        barcode
        title
        vendor
        vendor_addr
        vendor_tel
        website
        reserv_date
        img_url
'''

def db_insert_product(p, cur):
    # Transfer dict to row tuple
    row = (p['barcode'], p['title'].encode('utf-8'), p['main_cat'].encode('utf-8'), p['sub_cat'].encode('utf-8'), p['vendor'].encode('utf-8'), p['vendor_addr'].encode('utf-8'), p['vendor_tel'].encode('utf-8'), p['website'].encode('utf-8'), p['reserv_date'].encode('utf-8'), p['img_url'])

    try:
        cur.execute('DELETE from products WHERE barcode=?', (row[0],))
    except sqlite3.Error:
        # Ignore the error because
        traceback.print_exc()
        pass

    try:
        cur.execute('INSERT INTO products VALUES (?,?,?,?,?,?,?,?,?,?)', row)
        ret = 1

    except sqlite3.Error, e:
        print 'sqlite3.Error: '
        traceback.print_exc()
        pass

    print 'db_insert_product, ret = %d' % ret
    return ret


def db_insert_price(p, cur):
    # Transfer dict to row tuple
    row = (p['barcode'], p['price'].encode('utf-8'), p['ori_price'].encode('utf-8'), p['shop'].encode('utf-8'), p['description'].encode('utf-8'), p['website'].encode('utf-8'))

    try:
        cur.execute('DELETE from prices WHERE barcode=?', (row[0],))
    except sqlite3.Error:
        # Ignore the error because
        traceback.print_exc()
        pass

    try:
        cur.execute('INSERT INTO prices VALUES (?,?,?,?,?,?)', row)
        ret = 1

    except sqlite3.Error, e:
        print 'sqlite3.Error: '
        traceback.print_exc()
        pass

    print 'db_insert_price, ret = %d' % ret
    return ret

def db_insert_rows(products, db_name):

    inserted_row_count = 0

    try:
        conn = sqlite3.connect(db_name)

        cur = conn.cursor()

        conn.text_factory = str

    except sqlite3.Error:
        print 'sqlite3.Error:'
        traceback.print_exc()

    except Exception, e:
        traceback.print_exc()

    for p in products:
        ret = db_insert_product(p, cur)

        if ret > 0:
            ret = db_insert_price(p, cur)
            inserted_row_count += 1


    conn.commit()
    conn.close()

    return inserted_row_count



def db_create(db_name):

    try:
        #print "db_name=%s" % db_name
        conn = sqlite3.connect(db_name)

        cur = conn.cursor()

        try:
            # Create table
            cur.execute('''CREATE TABLE products
                             (barcode text PRIMARY KEY, title text, main_cat text, sub_cat text, vendor text, vendor_addr text, vendor_tel text, website text, reserv_date text, img_url text)''')
        except sqlite3.OperationalError:
            #print 'sqlite3.OperationalError: insert fail due to table exist '
            #traceback.print_exc()
            pass

        try:
            cur.execute('''CREATE TABLE prices
                             (barcode text PRIMARY KEY, price text, ori_price text, shop text, description text, ori_url text)''')
        except sqlite3.OperationalError:
            #print 'sqlite3.OperationalError: insert fail due to table exist '
            #traceback.print_exc()
            pass

    except sqlite3.OperationalError:
        print 'sqlite3.OperationalError: ... '
        traceback.print_exc()
        pass

    except Exception, e:
        traceback.print_exc()
        return False

    # Save (commit) the changes
    conn.commit()

    # We can also close the connection if we are done with it.
    # Just be sure any changes have been committed or they will be lost.
    conn.close()

    return True


def db_save_products(products, db_name = 'test.db'):

    ret = db_create(db_name)

    if not ret:
        return 0

    inserted_row_count = db_insert_rows(products, db_name)    

    return inserted_row_count


def db_merge(src_db, dest_db):

    try:
        print "insert into db %s from %s starts ..." % (dest_db, src_db)

        conn = sqlite3.connect(dest_db)

        cur = conn.cursor()

        cur.execute("attach '" + src_db + "' as src_db")

        # Insert all into dest_db_table
        cur.execute("insert into products select * from src_db.products")

        cur.execute("detach database src_db")

        print "insert into db %s from %s done" % (dest_db, src_db)


    except sqlite3.OperationalError:
        print 'sqlite3.OperationalError: insert fail '
        traceback.print_exc()
        pass

    except Exception, e:
        print 'sqlite3.OperationalError: insert other fail '
        traceback.print_exc()
        return False

    # Save (commit) the changes
    conn.commit()

    # We can also close the connection if we are done with it.
    # Just be sure any changes have been committed or they will be lost.
    conn.close()

    return True


if __name__ == '__main__':
    try:

        db_create('test.db');

        # products table
        ret = {}
        ret["main_cat"] = ""
        ret["sub_cat"] = ""
        ret["vendor"] = ""
        ret["vendor_addr"] = ""
        ret["vendor_tel"] = ""
        ret["barcode"] = ""
        ret["title"] = ""
        ret["reserv_date"] = ""
        ret["description"] = ""
        ret["img_url"] = "http://123/"
        ret["website"] = "http://website/"

        # prices table
        ret["shop"] = "六福香水(6lucky)"
        ret["price"] = "100"
        ret["ori_price"] = "150"

        products = []
        products.append(ret)
        
        db_save_products(products)

        sys.exit(0)

        print "done"
        sys.exit(0)

    except Exception, e:
        traceback.print_exc()
        sys.exit(-1)

