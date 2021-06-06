<?php

namespace Genre\Domain\MusicMetrics\Repository;

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
    public function __construct(ManagerRegistry $registry)
    {
        parent::__construct($registry, MusicMetrics::class);
    }

    // /**
    //  * @return MusicMetrics[] Returns an array of MusicMetrics objects
    //  */
    /*
    public function findByExampleField($value)
    {
        return $this->createQueryBuilder('m')
            ->andWhere('m.exampleField = :val')
            ->setParameter('val', $value)
            ->orderBy('m.id', 'ASC')
            ->setMaxResults(10)
            ->getQuery()
            ->getResult()
        ;
    }
    */

    /*
    public function findOneBySomeField($value): ?MusicMetrics
    {
        return $this->createQueryBuilder('m')
            ->andWhere('m.exampleField = :val')
            ->setParameter('val', $value)
            ->getQuery()
            ->getOneOrNullResult()
        ;
    }
    */
}
