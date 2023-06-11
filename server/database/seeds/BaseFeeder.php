<?php

use Illuminate\Database\Seeder;
use app\Base;

class BaseFeeder extends Seeder
{
    /**
     * Run the database seeds.
     *
     * @return void
     */
    public function run()
    {
        // Let's truncate our existing records to start from scratch.
        Base::truncate();

        $faker = \Faker\Factory::create();

        // And now, let's create a few articles in our database:
        for ($i = 0; $i < 20; $i++) {
            Base::create([
                'ip' => $faker->ipv4,
                'data' => $faker->tld,
            ]);
        }
    }
}
