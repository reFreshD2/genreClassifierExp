<?php

namespace Genre\Domain\MusicMetrics\Repository;

use Doctrine\ORM\EntityManagerInterface;
use Doctrine\ORM\OptimisticLockException;
use Doctrine\ORM\ORMException;
use Genre\Domain\MusicMetrics\Entity\MusicMetrics;
use Doctrine\Bundle\DoctrineBundle\Repository\ServiceEntityRepository;
use Doctrine\Persistence\ManagerRegistry;

/**
 * @method MusicMetrics|null find($id, $lockMode = null, $lockVersion = null)
 * @method MusicMetrics|null findOneBy(array $criteria, array $orderBy = null)
 * @method MusicMetrics[]    findAll()
 * @method MusicMetrics[]    findBy(array $criteria, array $orderBy = null, $limit = null, $offset = null)
 */
class MusicMetricsRepository extends ServiceEntityRepository
{
    private const MAP = [
        'рок' => [2, 101],
        'регги' => [102, 200],
        'поп' => [201, 298],
        'метал' => [299, 390],
        'джаз' => [391, 490],
        'хип-хоп' => [491, 588],
        'диско' => [589, 687],
        'кантри' => [688, 787],
        'классика' => [788, 887],
        'блюз' => [888, 987],
    ];
    private EntityManagerInterface $entityManager;

    public function __construct(ManagerRegistry $registry)
    {
        parent::__construct($registry, MusicMetrics::class);
        $this->entityManager = $this->getEntityManager();
    }

    /**
     * @throws OptimisticLockException
     * @throws ORMException
     */
    public function save(MusicMetrics $musicMetrics): void
    {
        $this->entityManager->persist($musicMetrics);
        $this->entityManager->flush();
    }

    public function getGenre(): array
    {
        return $this->createQueryBuilder('mm')
            ->select('mm.genre')
            ->addGroupBy('mm.genre')
            ->getQuery()
            ->getArrayResult();
    }

    public function getView(): array
    {
//        $genres = $this->createQueryBuilder('mm')
//            ->select('mm.genre')
//            ->addGroupBy('mm.genre')
//            ->getQuery()
//            ->getArrayResult();
//
//        $musicMetrics = [];
//        foreach ($genres as $genre) {
//            $builder = $this->createQueryBuilder('mm');
//            $genreMusicMetrics = $builder->andWhere($builder->expr()->eq('mm.genre', $genre['genre']))
//                ->getQuery()
//                ->getArrayResult();
//            $musicMetrics = array_merge($musicMetrics, $genreMusicMetrics);
//        }
//
//        return $musicMetrics;
        $ids = [
            random_int(self::MAP['рок'][0], self::MAP['рок'][1]),
            random_int(self::MAP['регги'][0], self::MAP['регги'][1]),
            random_int(self::MAP['поп'][0], self::MAP['поп'][1]),
            random_int(self::MAP['метал'][0], self::MAP['метал'][1]),
            random_int(self::MAP['джаз'][0], self::MAP['джаз'][1]),
            random_int(self::MAP['хип-хоп'][0], self::MAP['хип-хоп'][1]),
            random_int(self::MAP['диско'][0], self::MAP['диско'][1]),
            random_int(self::MAP['кантри'][0], self::MAP['кантри'][1]),
            random_int(self::MAP['классика'][0], self::MAP['классика'][1]),
            random_int(self::MAP['блюз'][0], self::MAP['блюз'][1]),
        ];
        $builder = $this->createQueryBuilder('mm');
        return $builder->andWhere($builder->expr()->in('mm.id', $ids))
            ->getQuery()
            ->getArrayResult();
    }
}
