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

    public function getView(): array
    {
        $count = count($this->findAll());
        if ($count > 10) {
            $firstRecord = $this->createQueryBuilder('mm')
                ->addOrderBy('mm.id', 'ASC')
                ->setMaxResults(5)
                ->getQuery()
                ->getArrayResult();
            $lastRecord = $this->createQueryBuilder('mm')
                ->addOrderBy('mm.id', 'ASC')
                ->setMaxResults(5)
                ->setFirstResult($count - 5)
                ->getQuery()
                ->getArrayResult();
            return array_merge($firstRecord, $lastRecord);
        }

        return $this->findAll();
    }
}
